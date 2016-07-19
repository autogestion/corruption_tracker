from pprint import pprint
import json


from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core.cache import cache
# from django.utils.translation import ugettext as _

from geoip2.errors import AddressNotFoundError

from utils.common import get_client_ip
from claim.models import OrganizationType
from corruption_tracker.middleware import SqlProfilingMiddleware


class MapPageView(View):
    template_name = 'map.html'

    def get(self, request):
        resp_dict = {
            'login_error': request.GET.get('login_error', 0),
            'page': 'single',
            'org_types': OrganizationType.objects.all().prefetch_related("claimtype_set"),
            'test_alarm': False}

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

        if settings.TEST_SERVER:
            resp_dict['test_alarm'] = True
        
        ip = get_client_ip(request)
        # cached_zoom = cache.get('lat_lon_for::%s' % ip)

        # if cached_zoom is not None:
        #     resp_dict['zoom_to']=cached_zoom
        # else:
        g = GeoIP2()
        try:
            if g.country(ip)['country_code'] == settings.COUNTRY_CODE:
                resp_dict['zoom_to'] = list(g.lat_lon(ip))
            else:
                resp_dict['zoom_to'] = settings.DEFAULT_ZOOM
        except AddressNotFoundError:
            resp_dict['zoom_to'] = settings.DEFAULT_ZOOM

            # cache.set('lat_lon_for::%s' % ip, resp_dict['zoom_to'])

        return render(request, self.template_name, resp_dict)


class LoginView(View):

    def get(self, request):
        return HttpResponseRedirect('/')

    def post(self, request):
        # login_form = AuthenticationForm(request, request.POST)
        # response_data = {}
        # if login_form.is_valid():
        #     response_data['result'] = 'Success!'
        #     response_data['message'] = 'You"re logged in'
        # else:
        #     response_data['result'] = 'failed'
        #     response_data['message'] = 'You messed up'

        # return HttpResponse(json.dumps(response_data), content_type="application/json")

        logout(request)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            url = reverse('single') + '?login_error=1'
            return HttpResponseRedirect(url)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def profiling(request):
    return render_to_response(
        "profiling.html", {"queries": SqlProfilingMiddleware.Queries})
