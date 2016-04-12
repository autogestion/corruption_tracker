
from django.conf.urls import url, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
# from rest_framework import generics

from api import views, claim, geoinfo



# from oauth2_provider import views as oauth2_views
# def add_to_swagger(object):
#     #add it to the class' base classes
#     object.__class__.__bases__ += (generics.GenericAPIView, )
#     return object


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
    # url(r'^sign_up/$', views.SignUp.as_view(), name="sign_up"),
    url(r'^', include('oauth2_provider.urls', namespace='oauth2_provider')),
    ]

# urlpatterns += oauth2_urlpatterns
# urlpatterns += (
    # url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    # url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    # url(r'^revoke_token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),    
    # url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
    # url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
    # url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
    # url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
    # url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    # url(r'^authorized_tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
    # url(r'^authorized_tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
    #     name="authorized-token-delete"),
    # ]

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
