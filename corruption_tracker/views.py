import json

from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe

from claim.models import Claim
from utils.common import read_map


def home(request):
    json_data = read_map()

    places = [{'data': b['properties']['ID'], 'value': b['properties']['NAME']}
              for b in json_data['features'] if b['properties']['NAME']]

    Claim.update_map(json_data)

    return render(
        request,
        'home.html',
        {'buildings': mark_safe(json.dumps(json_data)),
         'page': 'home',
         'places': mark_safe(json.dumps(places))})


def add_page(request):
    json_data = read_map()

    places = [{'data': b['properties']['ID'], 'value': b['properties']['NAME']}
              for b in json_data['features'] if b['properties']['NAME']]

    Claim.update_map(json_data)

    if settings.RECAPTCHA_ENABLED is False:
        settings.RECAPTCHA_PUBLIC = ''

    return render(
        request,
        'add_page.html',
        {'buildings': mark_safe(json.dumps(json_data)),
         'page': 'add_page',
         'places': mark_safe(json.dumps(places)),
         'recaptcha_public': settings.RECAPTCHA_PUBLIC})


def about(request):
    return render(request, 'about.html', {'page': 'about'})
