import json

from django.utils.safestring import mark_safe
from django.conf import settings

from geoinfo.models import Layer


def create_default_layer(claims=True):
    # There was an idea that we don't need
    # claims on add page

    try:
        layer = Layer.objects.get(is_default=True)
    except Layer.DoesNotExist:
        layer = Layer.objects.get(name=settings.DEFAULT_LAYER_NAME)
    polygons = layer.polygon_set.all()

    organizations = []
    for polygon in polygons:
        organizations.extend(polygon.organizations.all())

    places = [{'data': org.id, 'value': org.name}
              for org in organizations]

    data = []
    for polygon in polygons:
        data.append(polygon.generate_map_polygon())

    geo_json = {
        'type': "FeatureCollection", }
    geo_json['features'] = data

    return {'buildings': mark_safe(json.dumps(geo_json)),
            'places': mark_safe(json.dumps(places))}
