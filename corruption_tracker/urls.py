"""corruption_tracker URL Configuration"""

from django.conf.urls import include, url, static
from django.conf import settings
# from django.contrib import admin
from django.contrib.gis import admin
from django.views.static import serve
from django.views.i18n import javascript_catalog

from corruption_tracker import views

js_info_dict = {}

urlpatterns = [
    # Rest API
    url(r'^api/', include('api.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog'),

    url(r'^$', views.MapPageView.as_view(), name="single"),

    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/$', views.LoginView.as_view(),
        name='login'),

    url(r'^logout/$', views.logout_user,
        name='logout'),

    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^profiling/$', views.profiling),
        url(r'^press/', include('blog.urls')),
        url(r'^user/', include('interaction.urls')),
    ]
