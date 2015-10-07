import json

from django.utils.safestring import mark_safe


class LayerGenerator:

    def __init__(self, layer_obj):
        self.layer = layer_obj
        self.max_claims = layer_obj.max_claims

    def color_spot(self, value):
        percent = value * 100 / self.max_claims

        if percent <= 20:
            return 'green'
        elif percent <= 70:
            return 'yellow'
        else:
            return 'red'

    def generate(self):
        polygons = self.layer.polygon_set.all()

        organizations = []
        for polygon in polygons:
            organizations.extend(polygon.organizations.all())

        places = [{'data': org.id, 'value': org.name}
                  for org in organizations]

        data = []
        for polygon in polygons:
            polygon_json = polygon.generate_map_polygon()
            polygon_claims = polygon_json["properties"]['polygon_claims']
            polygon_json["properties"]['color'] = self.color_spot(polygon_claims)\
                if polygon_claims else 'grey'
            data.append(polygon_json)

        geo_json = {
            'type': "FeatureCollection",
            'config': {
                'center': json.loads(self.layer.center),
                'zoom': self.layer.zoom},
        }
        geo_json['features'] = data

        return {'buildings': mark_safe(json.dumps(geo_json)),
                'places': mark_safe(json.dumps(places))}
