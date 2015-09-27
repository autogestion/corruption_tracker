import json

from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from geoinfo.models import Layer
from utils.common import get_geojson_file


def create_default_layer(claims=True):
    # There was an idea that we don't need
    # claims on add page

    json_data = get_geojson_file()
    # places = [{'data': b['properties']['ID'], 'value': b['properties']['NAME']}
    #           for b in json_data['features'] if b['properties']['NAME']]

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
    json_data['features'] = data

    return {'buildings': mark_safe(json.dumps(json_data)),
            'places': mark_safe(json.dumps(places))}


def home(request):
    resp_dict = create_default_layer()
    resp_dict['page'] = 'home'

    return render(request, 'home.html', resp_dict)


def add_page(request):
    resp_dict = create_default_layer()
    resp_dict['page'] = 'add_page'

    if settings.RECAPTCHA_ENABLED is False:
        settings.RECAPTCHA_PUBLIC = ''
    resp_dict['recaptcha_public'] = settings.RECAPTCHA_PUBLIC

    return render(request, 'add_page.html', resp_dict)


def about(request):
    return render(request, 'about.html', {'page': 'about'})


def login_user(request):
    logout(request)
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('next', '/'))

    return render_to_response('auth/login.html',
                              context_instance=RequestContext(request))
