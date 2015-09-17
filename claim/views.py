import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from claim.models import Claim


def get_claims(request, polygon_id):
    # results = {'success':False}

    claims = Claim.objects.filter(polygon_id=polygon_id)

    if claims:
        claims_list = []
        for claim in claims:
            details = {'text': claim.text,
                       'servant': claim.servant,
                       'complainer': claim.complainer.username}
            claim_block = _("""Servant: %(servant)s<br>
                               Claim: %(text)s<br>
                               From: %(complainer)s<br><br>""") % details

            claims_list.append(claim_block)

        claims_html = ''.join(claims_list)

        results = {'success': True, 'claims': claims_html}

    else:
        results = {'success': True, 'claims': 'На цей заклад немає скарг'}

    return HttpResponse(json.dumps(results), content_type='application/json')


@login_required
def add_claim(request):
    code = 500
    if request.POST['polygon_id'] and request.POST['claim_text']:
        claim = Claim(text=request.POST['claim_text'],
                      polygon_id=request.POST['polygon_id'],
                      servant=request.POST['servant'],
                      # TODO(vegasq) Shouldn't we keep messages anonymously?
                      #              Privacy in such question really important,
                      #              if somehow this information will reach
                      #              incorrect people, it can ruin someones
                      #              life.
                      complainer=request.user)
        claim.save()
        # Correct insert code
        code = 201

    return HttpResponse(status=code)
