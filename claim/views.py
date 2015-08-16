import json

from django.http import HttpResponse

from claim.models import Claim


def get_claims(request, polygon_id):
    # results = {'success':False}

    claims = Claim.objects.filter(polygon_id=polygon_id)

    if claims:
        claims_html = ''
        for index, claim in enumerate(claims, 1):
            claims_html = claims_html + str(index) + '. ' + claim.text + '<br><br>'


        results = {'success':True, 'claims': claims_html}

    else:
        results = {'success':True, 'claims': 'No claims for this polygon'}

    return HttpResponse(json.dumps(results), content_type='application/json')




def add_claim(request): 
    results = {'success':False}

    if request.POST['polygon_id'] and request.POST['claim_text']:
        claim = Claim(text=request.POST['claim_text'],
                      polygon_id=request.POST['polygon_id'])
        claim.save()
        results = {'success':True} 


    return HttpResponse(json.dumps(results), content_type='application/json')