import json

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from claim.models import Claim


def get_claims(request, polygon_id):
    # results = {'success':False}
    try:
        claims = Claim.objects.filter(polygon_id=polygon_id)

        if claims:
            claims_list = []
            for claim in claims:
                details = {'text': claim.text, 'servant': claim.servant,
                            'complainer': claim.complainer.username,}
                claim_block = """Службовець: %(servant)s <br>
                                 Скарга: %(text)s    <br>
                                 Вiд: %(complainer)s   <br><br>""" %details

                claims_list.append(claim_block)
                
            claims_html = ''.join(claims_list)

            results = {'success':True, 'claims': claims_html}

        else:
            results = {'success':True, 'claims': 'No claims for this polygon'}
    except Exception as e:
        print(e)

    return HttpResponse(json.dumps(results), content_type='application/json')



@login_required
def add_claim(request): 
    results = {'success':False, 'text': 'Claim not added'}

    if request.POST['polygon_id'] and request.POST['claim_text']:
        claim = Claim(text=request.POST['claim_text'],
                      polygon_id=request.POST['polygon_id'],
                      servant=request.POST['servant'],
                      complainer=request.user)
        claim.save()
        results = {'success':True, 'text': 'Claim added'} 


    return HttpResponse(json.dumps(results), content_type='application/json')