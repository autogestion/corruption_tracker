from pprint import pprint

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
# from django.utils.translation import ugettext as _

# from geoinfo.views import LayerGenerator
from geoinfo.models import Polygon
from claim.models import OrganizationType


def add_page(request):
    resp_dict = Polygon.objects.get(is_default=True).generate_layer(add=True)
    resp_dict['page'] = 'add_page'

    if settings.RECAPTCHA_ENABLED is False:
        settings.RECAPTCHA_PUBLIC = ''
    resp_dict['recaptcha_public'] = settings.RECAPTCHA_PUBLIC

    test_alarm = None
    if settings.TEST_SERVER:
        test_alarm = '<p style="color:red">%s</p>' %'УВАГА! Ресурс працює в тестовому режимі. *'
    resp_dict['test_alarm'] = test_alarm

    # pprint(resp_dict['polygons'])
    return render(request, 'add_page.html', resp_dict)


def map(request):
    resp_dict = Polygon.objects.get(is_default=True).generate_layer()
    resp_dict['page'] = 'map'

    test_alarm = None
    if settings.TEST_SERVER:
        test_alarm = '<p style="color:red">%s</p>' %"*  Усі П.І.Б. посадовців та назви організацій уявні, співпадіння випадкові."
    resp_dict['test_alarm'] = test_alarm

    return render(request, 'map.html', resp_dict)


def about(request):
    return render(request, 'about.html', {'page': 'about'})


def single(request):
    resp_dict = Polygon.objects.get(is_default=True).generate_layer(add=True)
    resp_dict['page'] = 'single'

    resp_dict['org_types'] = OrganizationType.objects.all()
    print(resp_dict['org_types'], "resp_dict['org_types']")

    if settings.RECAPTCHA_ENABLED is False:
        settings.RECAPTCHA_PUBLIC = ''
    resp_dict['recaptcha_public'] = settings.RECAPTCHA_PUBLIC
    # pprint(resp_dict['polygons'])
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



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')