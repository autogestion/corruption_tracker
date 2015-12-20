"""corruption_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout
from django.views.static import serve


from claim import views as claim_views
from geoinfo import views as geo_views
# from geoinfo import serializers
from . import views as main_vies


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

    url(r'^login/$', main_vies.login_user,
        name='login'),
    url(r'^accounts/logout/$', logout,
        {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', main_vies.add_page, name="add_page"),
    url(r'^map$', main_vies.map, name="map"),
    url(r'^about$', main_vies.about, name="about"),

    # AJAX calls
    url(r'^get_claims/(?P<org_id>[\w.]{0,256})/limit=(?P<limit>\d+)/$',
        claim_views.get_claims, name="get_claims"),
    url(r'^get_claims/(?P<org_id>[\w.]{0,256})/$',
        claim_views.get_claims, name="get_claims"),
    url(r'^add_claim$', claim_views.add_claim, name="add_claim"),
    url(r'^claims/(?P<org_id>[\w.]{0,256})/$',
        claim_views.claims, name="claims"),

    # url(r'^export_layer/(?P<layer_id>[\w.]{0,256})/$',
    #     geo_views.export_layer, name="export_layer"),

    # Rest API
    # url(r'^v1/polygons$', serializers.PolygonView.as_view(),
    #     name='polygon-list'),
    url(r'^v1/get_polygons_tree/(?P<polygon_id>[\w.]{0,256})/$',
        geo_views.get_polygons_tree, name="get_polygons_tree"),




] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
