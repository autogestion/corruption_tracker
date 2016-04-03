
# from django.conf.urls import url, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views, claim, geoinfo

# from claim.models import Claim
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse


# @api_view(('GET',))
# def api_root(request, format=None):
#     return Response({
#         'get_polygons_tree': reverse('get_polygons_tree', request=request, format=format),
#         'get_nearest_polygons': reverse('get_nearest_polygons', request=request, format=format),
#         'check_in_building': reverse('check_in_building', request=request, format=format)
#     })


class CustomRouter(DefaultRouter):

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        if getattr(viewset, 'polygon', False):
            if viewset.polygon == 'get_nearest':
                return '(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)'
            elif viewset.polygon in ['check_in', 'fit_bounds']:
                return '(?P<layer>\d+)/(?P<coord>.*)'

        return super(CustomRouter,
                     self).get_lookup_regex(viewset, lookup_prefix)

router = CustomRouter()

urlpatterns = []


# ----    v1.2 api
# router.register(r'----------------1.2', views_1_1.ClaimViewSet, base_name='zdelimiter2')
router.register(r'claim', claim.ClaimViewSet,
                base_name='claims')
router.register(r'organization', claim.OrganizationViewSet,
                base_name='organizations')
router.register(r'polygon', geoinfo.PolygonViewSet,
                base_name='polygon')
router.register(r'polygon/get_nearest', geoinfo.GetNearestPolygons,
                base_name='get_nearest')
router.register(r'polygon/fit_bounds', geoinfo.FitBoundsPolygons,
                base_name='fit_bounds')
router.register(r'polygon/check_in', geoinfo.CheckInPolygon,
                base_name='check_in')
router.register(r'polygon/get_tree', geoinfo.GetPolygonsTree,
                base_name='get_polygons')
router.register(r'update', views.GetUpdatedViewSet,
                base_name='updated')

# router.register(r'v1.2/polygons', views.PolygonViewSet2, base_name='polygons2')

urlpatterns += router.urls
