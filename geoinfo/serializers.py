
from rest_framework import serializers, generics
from geoinfo.models import Polygon


class PolygonSerializer(serializers.ModelSerializer):
    # parentCategory = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Polygon
        # fields = ('subpolygons', 'polygon_id', 'address')
        fields = ('polygon_id', 'address')

# PolygonSerializer.base_fields['subpolygons'] = PolygonSerializer()


class PolygonView(generics.ListAPIView):

    model = Polygon
    serializer_class = PolygonSerializer


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
