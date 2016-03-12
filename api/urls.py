
from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework import viewsets

from api import views, views_1_1, views_1_2
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


# class zDelimiter(viewsets.ViewSet):
#     queryset = Claim.objects.all()


class CustomRouter(DefaultRouter):

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        if getattr(viewset, 'polygon', False):
            if viewset.polygon == 'get_nearest':
                return '(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)'
            elif viewset.polygon == 'check_in':
                return '(?P<layer>\d+)/(?P<coord>.*)'

        return super(CustomRouter, self).get_lookup_regex(viewset, lookup_prefix)



router = CustomRouter()

# -----   v1 api
router.register(r'v1/claims', views.ClaimViewSet)
router.register(r'v1/organizations', views.OrganizationViewSet)
router.register(r'v1/claim_types', views.ClaimTypeViewSet)


urlpatterns = [
	# url(r'^v1/$', api_root),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^v1/token/', obtain_auth_token, name='api-token'),
    url(r'^v1/get_polygons_tree/(?P<polygon_id>[\w.]{0,256})/$',
        views.get_polygons_tree, name="get_polygons_tree"),
    url(r'^v1/get_nearest_polygons/(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)$',
        views.get_nearest_polygons, name="get_nearest_polygons"),
    url(r'^v1/check_in_building/(?P<layer>\d+)/(?P<coord>.*)$',
        views.check_in_building, name="check_in_building"),
]

# ----    v1.1 api
router.register(r'----------------1.1', views_1_1.ClaimViewSet, base_name='zdelimiter1')
router.register(r'v1.1/claims', views_1_1.ClaimViewSet, base_name='claims')
router.register(r'v1.1/organizations', views_1_1.OrganizationViewSet, base_name='organizations')
router.register(r'v1.1/claim_types', views_1_1.ClaimTypeViewSet, base_name='claim_types')
router.register(r'v1.1/get_polygons_tree', views_1_1.GetPolygonsTree, base_name='get_polygons_tree')
router.register(r'v1.1/get_nearest_polygons', views_1_1.GetNearestPolygons, base_name='get_nearest_polygons')
router.register(r'v1.1/check_in_polygon', views_1_1.CheckInPolygon, base_name='check_in_polygon')
router.register(r'v1.1/add_organization', views_1_1.AddOrganization, base_name='add_organization')




# ----    v1.2 api
router.register(r'----------------1.2', views_1_1.ClaimViewSet, base_name='zdelimiter2')
router.register(r'v1.2/claim', views_1_2.ClaimViewSet, base_name='claims2')
router.register(r'v1.2/organization', views_1_2.OrganizationViewSet, base_name='organizations2')


# get_tree = views_1_2.PolygonViewSet.as_view({
#     'get': 'get_tree'
# })
# get_nearest = views_1_2.PolygonViewSet.as_view({
#     'get': 'get_nearest'
# })
# check_in = views_1_2.PolygonViewSet.as_view({
#     'get': 'check_in'
# })

# urlpatterns += [
#     url(r'^get_tree/(?P<polygon_id>[\w.]{0,256})/$', get_tree, name='get_tree'),
#     url(r'^get_nearest/(?P<layer>\d+)/(?P<distance>.*)/(?P<coord>.*)/$', get_nearest, name='get_nearest'),
#     url(r'^check_in/(?P<layer>\d+)/(?P<coord>.*)/$', check_in, name='check_in'),
# ]
# router.register(r'v1.2/polygon', views_1_2.PolygonViewSet, base_name='polygons')


router.register(r'v1.2/polygon/get_tree', views_1_2.GetPolygonsTree, base_name='get_polygons_tree2')
router.register(r'v1.2/polygon/get_nearest', views_1_2.GetNearestPolygons, base_name='get_nearest_polygons2')
router.register(r'v1.2/polygon/check_in', views_1_2.CheckInPolygon, base_name='check_in_polygon2')


urlpatterns += router.urls