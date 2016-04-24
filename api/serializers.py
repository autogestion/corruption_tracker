
import json
# from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import serializers

from claim.models import Claim, Organization, ClaimType,\
    OrganizationType
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

    complainer = serializers.ReadOnlyField(source='complainer.username')

    class Meta:
        model = Claim
        fields = ('text', 'created', 'live', 'organization',
                  'servant', 'complainer', 'claim_type', 'bribe'
                  )
        read_only_fields = ('created',)
        extra_kwargs = {'claim_type': {'required': True}}


class OrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = ('type_id', 'name', 'claim_types')


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type',
            'claims',
            'polygons'
        )
  


class PolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon

    def to_representation(self, instance):
        if instance.shape:
            geometry = json.loads(instance.shape.json)
            [x.reverse() for x in geometry["coordinates"][0]]  
        else:
            geometry = None

        centroid = list(instance.centroid.coords)
        centroid.reverse()   


        responce = {
            "type": "Feature",
            "properties": {
                "ID": instance.polygon_id,
                "centroid": centroid,
                'address': instance.address,
                'parent_id': instance.layer.polygon_id if instance.layer else None,
                'level': instance.level,
                "polygon_claims": instance.total_claims,
                'zoom' : instance.zoom,
                'color': instance.get_color
            },
            "geometry": geometry
        }

        if instance.level == instance.building:    
            queryset = instance.organizations.all()
            serializer = OrganizationSerializer(queryset, many=True)
            responce["properties"]["organizations"] = serializer.data
      
        return responce



class PolygonNoShapeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon

    def to_representation(self, instance):
        return instance.polygon_to_json(shape=False)



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
