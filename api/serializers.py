
import json
# from pprint import pprint

from django.contrib.auth.models import User
from rest_framework import serializers

from claim.models import Claim, Organization, ClaimType,\
    OrganizationType, AddressException
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
    @property
    def data(self):
        ret = super(SkipEmptyListSerializer, self).data
        return [x for x in ret if x]


class OrganizationSerializer(serializers.ModelSerializer):

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
                  'claims',
                  'polygons'
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
        kwargs['child'] = cls()
        return SkipEmptyListSerializer(*args, **kwargs)


class PolygonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Polygon

    def to_representation(self, instance, with_shape=True, dynamic=True):
        if with_shape and instance.shape:
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
                # 'zoom': instance.zoom,
            },
        }

        if dynamic:
            responce["properties"]["polygon_claims"] = instance.total_claims
            responce["properties"]['color'] = instance.get_color

        if with_shape:
            responce["geometry"] = geometry

        if instance.level == instance.building:
            queryset = instance.organizations.all()
            serializer = OrganizationSerializer(queryset, many=True)
            responce["properties"]["organizations"] = serializer.data

        return responce


class PolygonUpdateSerializer(PolygonSerializer):

    class Meta:
        model = Polygon

    def to_representation(self, instance):
        return super(PolygonUpdateSerializer,
                     self).to_representation(instance, with_shape=False,
                                             dynamic=False)


# class PolygonNoShapeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Polygon

#     def to_representation(self, instance):
#         return instance.polygon_to_json(shape=False)


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
