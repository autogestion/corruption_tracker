import json

from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db.models import Count

from claim.models import Claim


def home(request):
    json_file = open(settings.GEOJSON)
    json_data = json.load(json_file)
    # print(json_data)

    polygons_values = Claim.objects.values('polygon_id').annotate(count=Count('polygon_id'))
    polygons_dict = {}
    for values_dict in polygons_values:
        polygons_dict[values_dict['polygon_id']]=values_dict['count']
    print(polygons_dict)

    for polygon in json_data["features"]:        
        polygon['claim_count']=polygons_dict.get(str(polygon["properties"]["OSM_ID"]), 0)
        # print(polygons_dict.get(str(polygon["properties"]["OSM_ID"]), 0))
        # print(polygon)

    return render(request, 'map.html', {'buildings': mark_safe(json.dumps(json_data))})