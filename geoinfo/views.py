import json

from django.http import HttpResponse
from django.utils.safestring import mark_safe


# from geoinfo.models import Layer
from geoinfo.serializers import extractor

# def export_layer(request, layer_id):

#     layer = Layer.objects.get(id=layer_id)
#     layer_json = layer.generate_json(add=False)['polygons']
#     responce = HttpResponse(layer_json)
#     responce['Content-Disposition'] = 'attachment; filename=%s.json' % layer.name
#     return responce


def get_polygons_tree(request, polygon_id):
    data = mark_safe(json.dumps(extractor(polygon_id)))
    return HttpResponse(data, content_type='application/json')
