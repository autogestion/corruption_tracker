import time

from django.http import HttpResponse
from django.conf import settings

from utils.common import get_client_ip


class CachedRequests(object):
    @classmethod
    def get(cls):
        return cls()

    def __init__(self):
        if settings.USE_CACHING:
            # For those who develop on windows and not able to beat the drum
            import memcache
            self.mc = memcache.Client([settings.MEMCACHED_HOST], debug=1)

    def _set(self, ip, data):
        self.mc.set(ip, data,
                    time=settings.CLAIM_TIMEOUT_PERIOD)

    def _get(self, ip):
        return self.mc.get(ip)

    def can_i_create_claim(self, request):
        """
        Memcached store where keys is ip addresses of customers,
        and values is list of latest retries.
        """

        ip = get_client_ip(request)
        stored = self._get(ip)

        if not stored or type(stored) != list:
            self._set(ip, [time.time()])
            return True
        else:
            stored.append(time.time())
            self._set(ip, stored)

            return not len(stored) > settings.CLAIMS_PER_HOUR


def caching(view):
    # Check if from this IP claim creation is allowed.
    def _decorated(*args, **kwargs):
        if settings.USE_CACHING:
            request = args[0]
            if not CachedRequests.get().can_i_create_claim(request):
                return HttpResponse(status=403)
            else:
                return view(*args, **kwargs)
        else:
            return view(*args, **kwargs)
    return _decorated
