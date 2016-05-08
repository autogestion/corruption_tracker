from pprint import pprint
import json

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.safestring import mark_safe
# from django.utils.translation import ugettext as _

from utils.common import get_client_ip
# from geoinfo.models import Polygon
from claim.models import OrganizationType


def single(request):
    resp_dict = {}
    resp_dict['page'] = 'single'

    resp_dict['org_types'] = OrganizationType.objects.all()

    claim_type_sets = {}
    for org_type in resp_dict['org_types']:
        claim_type_set = []
        for claim_type in org_type.claimtype_set.all():
            claim_type_set.append({'id': claim_type.id,
                                  'value': claim_type.name})
        claim_type_sets[org_type.type_id] = claim_type_set

    resp_dict['claim_types'] = mark_safe(json.dumps(claim_type_sets))

    if settings.RECAPTCHA_ENABLED is False:
        settings.RECAPTCHA_PUBLIC = ''
    resp_dict['recaptcha_public'] = settings.RECAPTCHA_PUBLIC
    # pprint(resp_dict['polygons'])

    test_alarm = None
    if settings.TEST_SERVER:
        test_alarm = """<p style="color:red; padding-top: 5px; padding-left:15px;
        ">УВАГА! Ресурс працює в тестовому режимі. Усі П.І.Б. посадовців уявні,
         співпадіння випадкові.</p>"""
    resp_dict['test_alarm'] = test_alarm

    g = GeoIP2()
    try:
        test_coordinates = getattr(settings, 'TEST_COORDINATES')
        resp_dict['zoom_to'] = test_coordinates
    except AttributeError:
        ip = get_client_ip(request)
        if g.country(ip)['country_code'] == settings.COUNTRY_CODE:
            resp_dict['zoom_to'] = list(g.lat_lon(ip))
        else:
            resp_dict['zoom_to'] = settings.DEFAULT_ZOOM
    # pprint(resp_dict)

    return render(request, 'single.html', resp_dict)


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


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

# def add_page(request):
#     resp_dict = Polygon.objects.get(is_default=True).generate_layer(add=True)
#     resp_dict['page'] = 'add_page'

#     if settings.RECAPTCHA_ENABLED is False:
#         settings.RECAPTCHA_PUBLIC = ''
#     resp_dict['recaptcha_public'] = settings.RECAPTCHA_PUBLIC

#     test_alarm = None
#     if settings.TEST_SERVER:
#         test_alarm = '<p style="color:red">%s</p>' %'УВАГА! Ресурс працює в тестовому режимі. *'
#     resp_dict['test_alarm'] = test_alarm

#     # pprint(resp_dict['polygons'])
#     return render(request, 'add_page.html', resp_dict)


# def map(request):
#     resp_dict = Polygon.objects.get(is_default=True).generate_layer()
#     resp_dict['page'] = 'map'

#     test_alarm = None
#     if settings.TEST_SERVER:
#         test_alarm = '<p style="color:red">%s</p>' %"*  Усі П.І.Б. посадовців та назви організацій уявні, співпадіння випадкові."
#     resp_dict['test_alarm'] = test_alarm

#     return render(request, 'map.html', resp_dict)


# def about(request):
#     return render(request, 'about.html', {'page': 'about'})
