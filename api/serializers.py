
import json
from pprint import pprint

from django.contrib.auth.models import User
from django.db import models, connection
from rest_framework import serializers

from claim.models import Claim, Organization, ClaimType,\
    OrganizationType, AddressException
from geoinfo.models import Polygon
from api.sql import moderation_filter

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


class OrgsForPolySerializer(serializers.ListSerializer):

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data

        polygons = []
        polygons_with_orgs = []
        parents = []
        for item in iterable:
            item_obj, item_id = self.child.to_representation(item)
            polygons.append(item_obj)
            if item_id:
                polygons_with_orgs.append(item_id)

            if 'parent_id' in item_obj["properties"]:
                if item_obj["properties"]['parent_id'] not in parents:
                    parents.append(item_obj["properties"]['parent_id'])


        if polygons_with_orgs:
            max_claims_dict = Polygon.get_max_for_layers(parents)
            queryset = Organization.objects.filter(polygon__in=polygons_with_orgs)  

            serializer = OrganizationSerializer(queryset, many=True, 
                skip_address=True, dynamic=False)

            orgs = serializer.data
            org_ids = [x['id'] for x in orgs]

            cursor = connection.cursor()
            cursor.execute("""
                SELECT claim_organization.id, COUNT(claim_claim.id) AS claims FROM claim_organization 
                    LEFT OUTER JOIN claim_claim ON (claim_organization.id = claim_claim.organization_id) 
                    WHERE (claim_organization.id IN (%s) AND %s )
                    GROUP BY claim_organization.id                 
                """ % (','.join([str(x) for x in org_ids]), moderation_filter)
                )

            claims_for_orgs = dict(cursor.fetchall())

            for org in orgs:
                if org['id'] in claims_for_orgs:
                    org['claims']=claims_for_orgs[org['id']]
                else:
                    org['claims']=0

            for polygon in polygons:
                for org in orgs:
                    if polygon["properties"]['ID'] in org['polygons']:
                        if "organizations" in polygon["properties"]:
                            polygon["properties"]["organizations"].append(org)
                        else:
                            polygon["properties"]["organizations"]=[org]

            for polygon in polygons:
                if polygon["properties"]["level"]==4:
                    polygon["properties"]["polygon_claims"]=sum(
                    [x['claims'] for x in polygon["properties"]["organizations"]])

                    if 'parent_id' in polygon["properties"] and polygon["properties"]['parent_id'] in max_claims_dict:                                  
                        max_claims = max_claims_dict[polygon["properties"]['parent_id']]                 
                    else:
                        max_claims = 0

                    polygon["properties"]['color'] = Polygon.color_spot(polygon["properties"]["polygon_claims"], max_claims)\
                        if polygon["properties"]["polygon_claims"] else 'grey'



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

        id_for_orgs = None
        if instance.level == instance.building:
            id_for_orgs = instance.polygon_id
            # queryset = instance.organizations.all()
            # serializer = OrganizationSerializer(queryset, many=True, 
            #     skip_address=True, dynamic=True)

            # responce["properties"]["organizations"] = serializer.data
            # responce["properties"]["polygon_claims"]=sum(
            #     [x['claims'] for x in responce["properties"]["organizations"]])

        else:
            responce["properties"]["polygon_claims"] = instance.total_claims
            responce["properties"]['color'] = instance.get_color()

        return responce, id_for_orgs



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
