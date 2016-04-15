
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api import views, claim, geoinfo


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


urlpatterns = [
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]


# ----    v1.2 api
router.register(r'sign_up', views.SignUp,
                base_name='sign_up')
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


urlpatterns += router.urls
