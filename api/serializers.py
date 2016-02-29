
from rest_framework import serializers
# from rest_framework.reverse import reverse
from claim.models import Claim, Organization, ClaimType
from geoinfo.models import Polygon


class ClaimSerializer(serializers.ModelSerializer):


    complainer = serializers.ReadOnlyField(source='complainer.username')
    created = serializers.ReadOnlyField()

    class Meta:
        model = Claim
        fields = ('text', 'created', 'live', 'organization',
                  'servant', 'complainer', 'claim_type',
                  )


class OrganizationSerializer(serializers.ModelSerializer):

    # claims = serializers.PrimaryKeyRelatedField(many=True, queryset=Claim.objects.all())

    class Meta:
        model = Organization
        fields = ('id', 'name', 'org_type', 'total_claims', 
            # 'claims'
            # 'json_claims', 
            'claim_types'
            )



class ClaimTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimType
        fields = ('id', 'name', 'icon')


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
