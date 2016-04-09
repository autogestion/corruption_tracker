from rest_framework.test import APIRequestFactory



factory = APIRequestFactory(enforce_csrf_checks=True)
request = factory.post('/claim/', {'text': 'Покусали комарі',
                                    'claim_type': '2',
                                    'servant': 'Бабця',
                                    'live': 'true',
                                    'organization': '13',
                                    'bribe': '50'})
