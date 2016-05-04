"""corruption_tracker URL Configuration"""

from django.conf.urls import include, url, static
from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.views import logout
from django.views.static import serve

from claim import views as claim_views
from geoinfo import views as geo_views
from . import views as main_vies


urlpatterns = [
    # Rest API
    url(r'^api/', include('api.urls')),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),


    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

    url(r'^login/$', main_vies.login_user,
        name='login'),
    url(r'^logout/$', main_vies.logout_user,
        name='logout'),
    # url(r'^accounts/logout/$', logout,
    #     {'next_page': '/'}),
    # url(r'^accounts/', include('allauth.urls')),

    url(r'^add_page$', main_vies.add_page, name="add_page"),
    url(r'^map$', main_vies.map, name="map"),
    url(r'^about$', main_vies.about, name="about"),
    # url(r'^single$', main_vies.single, name="single"),
    url(r'^$', main_vies.single, name="single"),

    # AJAX calls
    url(r'^get_claims/(?P<org_id>[\w.]{0,256})/limit=(?P<limit>\d+)/$',
        claim_views.get_claims, name="get_claims"),
    url(r'^get_claims/(?P<org_id>[\w.]{0,256})/$',
        claim_views.get_claims, name="get_claims"),
    url(r'^add_claim$', claim_views.add_claim, name="add_claim"),
    url(r'^add_org$', geo_views.add_org, name="add_org"),
    url(r'^claims/(?P<org_id>[\w.]{0,256})/$',
        claim_views.claims, name="claims"),

    # url(r'^export_layer/(?P<layer_id>[\w.]{0,256})/$',
    #     geo_views.export_layer, name="export_layer"),





] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
