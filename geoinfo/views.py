
from django.http import HttpResponse
from django.contrib.gis.geos import fromstr
from django.db.models.signals import post_save, post_delete
from geoinfo.models import Polygon
from claim.models import Claim, Organization, OrganizationType


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




def increment_claims(sender, instance, created, **kwargs):
    if created:
        houses = instance.organization.polygon_set.all()
        for house in houses:
            house.claims += 1
            house.save()
            # add to district
            house.layer.claims += 1
            house.layer.save()
            # add to city
            house.layer.layer.claims += 1
            house.layer.layer.save()
            # add to region
            house.layer.layer.layer.claims += 1
            house.layer.layer.layer.save()       

# post_save.connect(increment_claims, sender=Claim)



def decrement_claims(sender, instance, **kwargs):
    houses = instance.organization.polygon_set.all()
    print(houses)
    for house in houses:
        house.claims -= 1
        house.save()
        # sub from district
        house.layer.claims -= 1
        house.layer.save()
        # sub from city
        house.layer.layer.claims -= 1
        house.layer.layer.save()
        # sub from region
        house.layer.layer.layer.claims -= 1
        house.layer.layer.layer.save()       

# post_delete.connect(decrement_claims, sender=Claim)