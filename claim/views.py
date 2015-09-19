import requests

from django.http import HttpResponse
from django.conf import settings

from claim.models import Claim
from utils.common import get_client_ip
from utils.caching import caching



def get_claims(request, polygon_id):
    data = Claim.get_json_by_organization(polygon_id)
    return HttpResponse(data, content_type='application/json')


@caching
def add_claim(request, deny=False):
    
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
