
from rest_framework import permissions
from rest_framework.throttling import SimpleRateThrottle

from claim.models import Moderator


class IsAuthenticatedOrCreate(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)



class IsSafe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET',):
            return True
        return False

    def has_permission(self, request, view):
        if request.method in ('GET',):
            return True
        return False


class CanPost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('POST', 'GET'):
            return True
        return False

    def has_permission(self, request, view):
        if request.method in ('POST', 'GET'):
            return True
        return False


class PostThrottle(SimpleRateThrottle):    

    scope = 'post_throttle'

    def __init__(self):
        self.moderator = Moderator.get_moderator()
        super(PostThrottle, self).__init__()


    def get_rate(self):
        return '%d/hour' % self.moderator.claims_per_hour


    def get_cache_key(self, request, view):        
        if request.method == 'POST' and self.moderator.use_memcached:
            return self.cache_format % {
                'scope': self.scope,
                'ident': self.get_ident(request)
            }
        else:
            return None