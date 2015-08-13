import json

from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe


def home(request):
	json_file = open(settings.GEOJSON)
	json_data = json.load(json_file)
	# print(json_data)
	return render(request, 'map.html', {'buildings': mark_safe(json.dumps(json_data))})