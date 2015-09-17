import json
import requests

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from claim.models import Claim


# TODO(vegasq) Need create utils module, or something similar.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_claims(request, polygon_id):
    # results = {'success':False}

    claims = Claim.objects.filter(polygon_id=polygon_id)

    if claims:
        claims_list = []
        for claim in claims:
            details = {
                'text': claim.text,
                'servant': claim.servant,
                'complainer': _("Anonymous") if claim.complainer is None
                else claim.complainer.username
            }
            claim_block = _("""Servant: %(servant)s<br>
                               Claim: %(text)s<br>
                               From: %(complainer)s<br><br>""") % details

            claims_list.append(claim_block)

        claims_html = ''.join(claims_list)

        results = {'success': True, 'claims': claims_html}

    else:
        results = {'success': True, 'claims': 'На цей заклад немає скарг'}

    return HttpResponse(json.dumps(results), content_type='application/json')


def add_claim(request):
    if settings.RECAPTCHA_ENABLED and not request.user.is_authenticated():
        if not request.POST.get('g-recaptcha-response', False):
            raise Exception('Google reCaptcha verification not passed')

        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            {
                "secret": settings.RECAPTCHA_SECRET,
                "response": request.POST.get('g-recaptcha-response', False),
                "remoteip": get_client_ip(request)
            }
        ).json()

        if not response['success']:
            raise Exception('Google think user is not real.')

    user = None if request.POST.get(
        'anonymously',
        False) or not request.user.is_authenticated() else request.user

    code = 500
    if (
        request.POST.get('polygon_id', False) and
        request.POST.get('claim_text', False)
    ):
        claim = Claim(text=request.POST.get('claim_text', False),
                      polygon_id=request.POST.get('polygon_id', False),
                      servant=request.POST.get('servant', False),
                      complainer=user)
        claim.save()
        # Correct insert code
        code = 201

    return HttpResponse(status=code)
