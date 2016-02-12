import json

from django.http import HttpResponse
from django.utils.safestring import mark_safe


from geoinfo.models import Polygon
from geoinfo.serializers import extractor
from claim.models import Organization, OrganizationType


# def export_layer(request, layer_id):

#     layer = Layer.objects.get(id=layer_id)
#     layer_json = layer.generate_json(add=False)['polygons']
#     responce = HttpResponse(layer_json)
#     responce['Content-Disposition'] = 'attachment; filename=%s.json' % layer.name
#     return responce


def get_polygons_tree(request, polygon_id):
    data = mark_safe(json.dumps(extractor(polygon_id)))
    return HttpResponse(data, content_type='application/json')


def add_org(request):
    print(request.POST)

    layer = Polygon.objects.get(
        polygon_id=request.POST['layer_id'])

    polygon = Polygon(
        polygon_id=request.POST['centroid'],
        centroid=request.POST['centroid'],
        address=request.POST['address'],
        layer=layer,
        level=Polygon.building,
        zoom=17,
        is_verified=True)
    polygon.save()

    org_type = OrganizationType.objects.get(
        type_id=request.POST['org_type'])

    organization = Organization(
        name=request.POST['org_name'],
        org_type=org_type)
    organization.save()

    polygon.organizations.add(organization)

    return HttpResponse(status=201)
