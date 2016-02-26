import json
import requests

from django.http import HttpResponse
from django.conf import settings
from django.utils.html import escape
from django.shortcuts import render

from claim.models import Claim, Organization, ClaimType
from utils.common import get_client_ip
from utils.caching import caching


def get_claims(request, org_id, limit=999):
    # For unknown reason django do not check type param, event if in urls.py
    # we have coorect \d pattern.
    limit = int(limit)
    data = json.dumps(Organization.objects.get(id=org_id).json_claims(limit=limit))
    return HttpResponse(data, content_type='application/json')


def claims(request, org_id):
    return render(request, 'claims.html', {'org_id': org_id})


@caching
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
        request.POST.get('org_id', False) and
        request.POST.get('claim_text', False)
    ):
        claim = Claim(
            text=escape(request.POST.get('claim_text', False)),
            servant=escape(request.POST.get('servant', False)),
            bribe=escape(request.POST.get('bribe', 0)),
            complainer=user,
            organization=Organization.objects.get(
                id=request.POST.get('org_id', False)),
            claim_type=ClaimType.objects.get(
                id=request.POST.get('claim_type', False)),
            moderation=user and 'not_moderated' or 'anonymous',
        )
        claim.save()
        # Correct insert code
        code = 201

    return HttpResponse(status=code)
