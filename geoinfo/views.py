
from django.http import HttpResponse

from geoinfo.models import Layer


def export_layer(request, layer_id):

    layer = Layer.objects.get(id=layer_id)
    layer_json = layer.generate_json(add=False)['polygons']
    responce = HttpResponse(layer_json)
    responce['Content-Disposition'] = 'attachment; filename=%s.json' % layer.name
    return responce
