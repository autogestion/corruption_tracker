import json

from django.utils.safestring import mark_safe


def generate_layer(layer_obj, claims=True):
    # There was an idea that we don't need
    # claims on add page

    polygons = layer_obj.polygon_set.all()

    organizations = []
    for polygon in polygons:
        organizations.extend(polygon.organizations.all())

    places = [{'data': org.id, 'value': org.name}
              for org in organizations]

    data = []
    for polygon in polygons:
        data.append(polygon.generate_map_polygon())

    geo_json = {
        'type': "FeatureCollection",
        'config': {
            'center': json.loads(layer_obj.center),
            'zoom': layer_obj.zoom},
    }
    geo_json['features'] = data

    return {'buildings': mark_safe(json.dumps(geo_json)),
            'places': mark_safe(json.dumps(places))}
