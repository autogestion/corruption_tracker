
from django.http import HttpResponse
from django.contrib.gis.geos import fromstr

from geoinfo.models import Polygon
from claim.models import Organization, OrganizationType


# def export_layer(request, layer_id):

#     layer = Layer.objects.get(id=layer_id)
#     layer_json = layer.generate_json(add=False)['polygons']
#     responce = HttpResponse(layer_json)
#     responce['Content-Disposition'] = 'attachment; filename=%s.json' % layer.name
#     return responce

def add_org(request):
    print(request.POST)

    layer = Polygon.objects.get(
        polygon_id=request.POST['layer_id'])

    polygon = Polygon(
        polygon_id=request.POST['centroid'],
        centroid=fromstr("POINT(%s %s)" % tuple(request.POST['centroid'].split(','))),
        shape=request.POST['shape'],
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
