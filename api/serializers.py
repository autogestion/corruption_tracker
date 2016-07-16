# import time
# import json
from pprint import pprint

from django.contrib.auth.models import User
from django.db import models
from django.forms.models import model_to_dict
from rest_framework import serializers


from claim.models import Claim, Organization, ClaimType,\
    OrganizationType, AddressException
from claim.sql import get_sum_for_layers, get_max_for_layers
from geoinfo.models import Polygon


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class ClaimTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimType
        fields = '__all__'


class ClaimListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [
            self.child.to_representation(item) for item in iterable if item
        ]


class ClaimSerializer(serializers.ModelSerializer):

    organization_name = serializers.ReadOnlyField(source='organization.name')
    claim_type_name = serializers.ReadOnlyField(source='claim_type.name')
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                        read_only=True)

    complainer_name = serializers.SerializerMethodField()
    claim_icon = serializers.SerializerMethodField()

    def get_complainer_name(self, instance):
        if instance.complainer:
            if instance.complainer.get_full_name():
                return instance.complainer.get_full_name()
            else:
                return instance.complainer.username

    def get_claim_icon(self, instance):
        if instance.claim_type and instance.claim_type.icon:
            return instance.claim_type.icon.url

    class Meta:
        model = Claim
        fields = ('servant', 'claim_type_name', 'bribe',
                  'text', 'created', 'live', 'claim_icon',
                  # write only
                  'organization', 'claim_type',
                  # changing
                  'organization_name',
                  'complainer', 'complainer_name',)

        extra_kwargs = {'claim_type': {'required': True, 'write_only': True},
                        'organization': {'write_only': True},
                        'complainer': {'read_only': True},
                        'claim_icon': {'read_only': True}, }

    def to_representation(self, instance):
        claim = super(ClaimSerializer, self).to_representation(instance)

        if self.org_or_user == 'org':
            claim['complainer_count'] = instance.num_c

        return claim

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls(**kwargs)
        kwargs.pop('org_or_user', None)
        return ClaimListSerializer(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.org_or_user = kwargs.pop('org_or_user', False)
        super(ClaimSerializer, self).__init__(*args, **kwargs)

        if self.org_or_user == 'org':
            self.fields.pop('organization_name', None)
        elif self.org_or_user == 'user':
            pass


class OrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = ('type_id', 'name', 'claim_types')


class SkipEmptyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        return [
            self.child.to_representation(item) for item in iterable if item
        ]


class OrganizationSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        dynamic = kwargs.pop('dynamic', False)
        skip_address = kwargs.pop('skip_address', False)
        super(OrganizationSerializer, self).__init__(*args, **kwargs)
        if not dynamic:
            self.fields.pop('claims', None)
        if skip_address:
            self.fields.pop('address', None)
            self.fields.pop('polygons', None)

    address = serializers.CharField()

    centroid = serializers.CharField(write_only=True)
    parent_polygon_id = serializers.CharField(write_only=True, required=False)
    polygon_id = serializers.CharField(write_only=True, required=False)
    shape = serializers.CharField(write_only=True, required=False)
    level = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type',
                  # from other tables
                  'address', 'polygons', 'claims',
                  # write only (for ploygon)
                  'parent_polygon_id', 'polygon_id',
                  'shape', 'level', 'centroid'
                  )
        extra_kwargs = {'org_type': {'required': True}}

    def to_representation(self, instance):
        try:
            return super(OrganizationSerializer,
                         self).to_representation(instance)
        except AddressException:
            pass

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls(**kwargs)
        kwargs.pop('dynamic', None)
        kwargs.pop('skip_address', None)
        return SkipEmptyListSerializer(*args, **kwargs)


class PolgygonBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon

    def to_representation(self, instance):
        centroid = list(instance.centroid.coords)
        centroid.reverse()

        responce = {
            "type": "Feature",
            "properties": {
                "ID": instance.polygon_id,
                "centroid": centroid,
                'address': instance.address,
                'parent_id': instance.layer_id,
                'level': instance.level,
            },
        }
        return responce


def level_separator(item_obj, parents, ids, poly_objects):
    ids.append(item_obj["properties"]['ID'])
    poly_objects.append(item_obj)
    if 'parent_id' in item_obj["properties"]:
        if item_obj["properties"]['parent_id'] not in parents:
            parents.append(item_obj["properties"]['parent_id'])


def level_appender(polygon, claims_dict, max_claims_dict):
    if polygon["properties"]["ID"] in claims_dict:
        polygon["properties"]["polygon_claims"] = claims_dict[polygon["properties"]["ID"]]
    else:
        polygon["properties"]["polygon_claims"] = 0

    if 'parent_id' in polygon["properties"] and polygon["properties"]['parent_id'] in max_claims_dict:
        max_claims = max_claims_dict[polygon["properties"]['parent_id']]
    else:
        max_claims = 0

    polygon["properties"]['color'] = Polygon.color_spot(polygon["properties"]["polygon_claims"], max_claims)\
        if polygon["properties"]["polygon_claims"] else 'grey'


class OrgsForPolySerializer(serializers.ListSerializer):

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        polygons = []
        buildings_parents, buildings_ids, buildings_objects = [], [], []
        district_parents, district_ids, district_objects = [], [], []
        area_parents, area_ids, area_objects = [], [], []
        region_ids, region_objects = [], []

        # start = time.time()
        for item in iterable:
            # start_repr = time.time()
            item_obj = self.child.to_representation(item)

            # print('      to representaion', time.time() - start_repr)
            level = item_obj["properties"]['level']
            if level == 4:
                # start_repr = time.time()
                level_separator(item_obj, buildings_parents, buildings_ids, buildings_objects)
                # print('      level_separator', time.time() - start_repr)
            elif level == 3:
                level_separator(item_obj, district_parents, district_ids, district_objects)
            elif level == 2:
                level_separator(item_obj, area_parents, area_ids, area_objects)
            elif level == 1:
                region_ids.append(item_obj["properties"]['ID'])
                region_objects.append(item_obj)
        # print('    separating by levels', time.time() - start)

        # ------------------------------Process buildings ---------------------
        if buildings_ids:
            org_ids = []
            # start = time.time()
            for polygon in buildings_objects:
                for org in polygon["properties"]["organizations"]:
                    if org['id'] not in org_ids:
                        org_ids.append(org['id'])
            # print('    getting org ids', time.time() - start)

            # start = time.time()
            claims_for_orgs = get_sum_for_layers(org_ids, 4)
            # print('    agregating claims(sql)', time.time() - start)

            # start = time.time()
            buildings_max_claims_dict = get_max_for_layers(buildings_parents, 4)
            # print('    agregating max claims(sql)', time.time() - start)

            for polygon in buildings_objects:
                for org in polygon["properties"]["organizations"]:
                    if org['id'] in claims_for_orgs:
                        org['claims'] = claims_for_orgs[org['id']]
                    else:
                        org['claims'] = 0

                polygon["properties"]["polygon_claims"] = sum(
                    [x['claims'] for x in polygon["properties"]["organizations"]])

                if 'parent_id' in polygon["properties"] and polygon["properties"]['parent_id'] in buildings_max_claims_dict:
                    max_claims = buildings_max_claims_dict[polygon["properties"]['parent_id']]
                else:
                    max_claims = 0

                polygon["properties"]['color'] = Polygon.color_spot(polygon["properties"]["polygon_claims"], max_claims)\
                    if polygon["properties"]["polygon_claims"] else 'grey'

            polygons += buildings_objects

        # ---------------------- Process districts -----------------------
        if district_ids:

            claims_for_houses = get_sum_for_layers(district_ids, 3)
            district_max_claims_dict = get_max_for_layers(district_parents, 3)
            for polygon in district_objects:
                level_appender(polygon, claims_for_houses, district_max_claims_dict)

            polygons += district_objects

        # ---------------------- Process cities -----------------------
        if area_ids:

            claims_for_areas = get_sum_for_layers(area_ids, 2)
            area_max_claims_dict = get_max_for_layers(area_parents, 2)
            for polygon in area_objects:
                level_appender(polygon, claims_for_areas, area_max_claims_dict)

            polygons += area_objects

        # ---------------------- Process regions -----------------------
        if region_ids:

            claims_for_regions = get_sum_for_layers(region_ids, 1)
            region_max_claims_dict = get_max_for_layers(['root'], 1)
            for polygon in region_objects:
                level_appender(polygon, claims_for_regions, region_max_claims_dict)

            polygons += region_objects

        return polygons


class PolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        return OrgsForPolySerializer(*args, **kwargs)

    def to_representation(self, instance):

        # start = time.time()
        # centroid = list(instance.centroid.coords)
        # print('        process_centroid', time.time() - start)

        # start = time.time()
        wkt = instance.centroid.wkt
        wkt = wkt[7:wkt.find(")")]
        centroid = [float(x) for x in wkt.strip().split(' ')]
        centroid.reverse()
        # print('        process_centroid wkt', time.time() - start)

        # start = time.time()
        responce = {
            "type": "Feature",
            "properties": {
                "ID": instance.polygon_id,
                "centroid": centroid,
                'address': instance.address,
                'parent_id': instance.layer_id,
                'level': instance.level,
            },
        }
        # print('        process_responce', time.time() - start)

        if instance.level == 4:

            # start = time.time()
            # orgs = OrganizationSerializer(
            #             instance.organizations.all(), many=True,
            #             skip_address=True, dynamic=False).data
            # print('        process orgs', time.time() - start)

            # start = time.time()
            orgs = instance.organizations.all()
            orgs = [model_to_dict(x, fields=['id', 'name', 'org_type']) for x in orgs]
            # print('        process orgs manually', time.time() - start)

            responce["properties"]["organizations"] = orgs

        # start = time.time()
        if instance.shape:

            # start_js = time.time()
            wkt = instance.shape.wkt
            wkt = wkt[10:wkt.find("))")]
            responce["geometry"] = {'type': 'Polygon',
                                    'coordinates':
                [[[float(y) for y in x.strip().strip(')').strip('(').split(' ')] for x in wkt.split(',')]]
            }
            # print('          getting shape wkt', time.time() - start_js)

            # start_js = time.time()
            # shape_json = instance.shape.json
            # responce["geometry"] = json.loads(shape_json)
            # print('          json shape', time.time() - start_js)

            [x.reverse() for x in responce["geometry"]["coordinates"][0]]
            # print(responce["geometry"])
        else:
            responce["geometry"] = None
        # print('        process_geometry', time.time() - start)

        return responce


def extractor(polygon_id):
    responce = {}
    polygon = Polygon.objects.get(polygon_id=polygon_id)
    if polygon.level == 4:
        orgs = {x.id: [x.name, x.org_type.name] for x in polygon.organizations.all()}
        responce[polygon.polygon_id] = {'address': polygon.address,
                                        'orgs': orgs}
        return responce
    else:
        responce[polygon.polygon_id] = {'address': polygon.address,
                                        'childs': {}}
        childs = polygon.polygon_set.all()
        for child in childs:
            responce[polygon.polygon_id]['childs'].update(extractor(child.polygon_id))

        return responce
