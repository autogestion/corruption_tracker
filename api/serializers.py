
import json
from pprint import pprint

from django.contrib.auth.models import User
from django.db import models
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
        fields = ('text', 'created', 'live', 'organization',
                  'organization_name', 'claim_type_name',
                  'servant', 'complainer', 'complainer_name',
                  'claim_type', 'bribe', 'claim_icon')
        extra_kwargs = {'claim_type': {'required': True},
                        'complainer': {'read_only': True}}


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

    centroid = serializers.CharField(write_only=True)
    address = serializers.CharField()

    parent_polygon_id = serializers.CharField(write_only=True, required=False)
    polygon_id = serializers.CharField(write_only=True, required=False)
    shape = serializers.CharField(write_only=True, required=False)
    level = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type',
                  'centroid', 'address',
                  'parent_polygon_id', 'polygon_id',
                  'shape', 'level',                  
                  'polygons', 
                  'claims'
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
        polygon["properties"]["polygon_claims"]=claims_dict[polygon["properties"]["ID"]]
    else:
        polygon["properties"]["polygon_claims"]=0

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
        buildings_parents, buildings_ids, buildings_objects = [],[],[]
        district_parents, district_ids, district_objects = [],[],[]
        area_parents, area_ids, area_objects = [],[],[]
        region_ids, region_objects = [],[]

        for item in iterable:
            item_obj = self.child.to_representation(item)  
            level = item_obj["properties"]['level']
            if level ==4:
                level_separator(item_obj, buildings_parents, buildings_ids, buildings_objects)
            elif level ==3:
                level_separator(item_obj, district_parents, district_ids, district_objects)
            elif level ==2:
                level_separator(item_obj, area_parents, area_ids, area_objects) 
            elif level ==1:
                region_ids.append(item_obj["properties"]['ID'])
                region_objects.append(item_obj)                


        # ------------------------------Process buildings -----------------------
        if buildings_ids:
            
            queryset = Organization.objects.filter(polygon__in=buildings_ids)  

            serializer = OrganizationSerializer(queryset, many=True, 
                skip_address=True, dynamic=False)

            orgs = serializer.data
            org_ids = [x['id'] for x in orgs]
            claims_for_orgs = get_sum_for_layers(org_ids, 4)

            for org in orgs:
                if org['id'] in claims_for_orgs:
                    org['claims']=claims_for_orgs[org['id']]
                else:
                    org['claims']=0


            for polygon in buildings_objects:
                for org in orgs:
                    if polygon["properties"]['ID'] in org['polygons']:
                        if "organizations" in polygon["properties"]:
                            polygon["properties"]["organizations"].append(org)
                        else:
                            polygon["properties"]["organizations"]=[org]


            buildings_max_claims_dict = get_max_for_layers(buildings_parents, 4)            
            for polygon in buildings_objects:
                polygon["properties"]["polygon_claims"]=sum(
                [x['claims'] for x in polygon["properties"]["organizations"]])

                if 'parent_id' in polygon["properties"] and polygon["properties"]['parent_id'] in buildings_max_claims_dict:                                  
                    max_claims = buildings_max_claims_dict[polygon["properties"]['parent_id']]                 
                else:
                    max_claims = 0

                polygon["properties"]['color'] = Polygon.color_spot(polygon["properties"]["polygon_claims"], max_claims)\
                    if polygon["properties"]["polygon_claims"] else 'grey'


            polygons += buildings_objects

        # ---------------------- Process districts -----------------------
        elif district_ids:

            claims_for_houses = get_sum_for_layers(district_ids, 3)
            district_max_claims_dict = get_max_for_layers(district_parents, 3)
            for polygon in district_objects:
                level_appender(polygon, claims_for_houses, district_max_claims_dict)

            polygons += district_objects


        # ---------------------- Process cities -----------------------
        elif area_ids:

            claims_for_areas = get_sum_for_layers(area_ids, 2)
            area_max_claims_dict = get_max_for_layers(area_parents, 2)
            for polygon in area_objects:
                level_appender(polygon, claims_for_areas, area_max_claims_dict)

            polygons += area_objects


        # ---------------------- Process regions -----------------------
        elif region_ids:

            claims_for_regions =  get_sum_for_layers(region_ids, 1)
            region_max_claims_dict = get_max_for_layers(['root'], 1)
            for polygon in region_objects:
                level_appender(polygon, claims_for_regions, region_max_claims_dict)

            polygons += region_objects


        return polygons


class PolygonSerializer(PolgygonBaseSerializer):

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs['child'] = cls()
        return OrgsForPolySerializer(*args, **kwargs)


    def to_representation(self, instance):
        responce = super(PolygonSerializer,
                     self).to_representation(instance)
        if instance.shape:
            responce["geometry"] = json.loads(instance.shape.json)
            [x.reverse() for x in responce["geometry"]["coordinates"][0]]
        else:
            responce["geometry"] = None            

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
