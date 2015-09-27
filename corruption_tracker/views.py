
from django.conf import settings
from django.http import *
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout

from geoinfo.views import create_default_layer


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
