import time

from django.http import HttpResponse
from django.conf import settings
from claim.models import Moderator, ModerationStatus, Claim

from utils.common import get_client_ip

moderator = Moderator.objects.get(id=1)
suspicous = ModerationStatus.objects.get(status_id="suspicious")


class CachedRequests(object):
    @classmethod
    def get(cls):
        return cls()

    def __init__(self):
        self.moderator = moderator
        if self.moderator.use_memcached:
            # if settings.USE_CACHING:
            # For those who develop on windows and not able to beat the drum
            import memcache
            self.mc = memcache.Client([settings.MEMCACHED_HOST], debug=1)

    def _set(self, ip, data):
        self.mc.set(ip, data,
                    # time=settings.CLAIM_TIMEOUT_PERIOD)
                    self.moderator.memcached_timeout)

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

            # return not len(stored) > settings.CLAIMS_PER_HOUR
            return not len(stored) > self.moderator.claims_per_hour


def caching(view):
    # Check if from this IP claim creation is allowed.
    def _decorated(*args, **kwargs):
        # if settings.USE_CACHING:
        if moderator.use_memcached:
            request = args[0]
            if not CachedRequests.get().can_i_create_claim(request):
                if not request.user.is_anonymous():
                    claims_to_mark = Claim.objects.filter(
                        complainer=request.user).\
                        order_by('-created')[:moderator.claims_per_hour]
                    for claim in claims_to_mark:
                        claim.moderation = suspicous
                        claim.save()

                return HttpResponse(status=403)
            else:
                return view(*args, **kwargs)
        else:
            return view(*args, **kwargs)
    return _decorated
