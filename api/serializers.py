from pprint import pprint

from rest_framework import serializers
# from rest_framework.reverse import reverse
from claim.models import Claim, Organization, ClaimType,\
    OrganizationType
from geoinfo.models import Polygon



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


class OrganizationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganizationType
        fields = ('type_id', 'name', 'claim_types')



class OrganizationSerializer(serializers.ModelSerializer):

    # claims = serializers.PrimaryKeyRelatedField(many=True, queryset=Claim.objects.all())

    # polygons = serializers.CharField(max_length=2000000)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type', 'total_claims', 
            # 'claims'
            # 'json_claims', 
            # 'claim_types'       
            'polygons'
            )


class PolygonSerializer(serializers.ModelSerializer):

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
