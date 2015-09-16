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
from django.conf.urls import include, url
from django.contrib import admin

from claim import views as claim_views
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', views.home, name="home"),
    url(r'^add_page$', views.add_page, name="add_page"),
    url(r'^about$', views.about, name="about"),

    # AJAX calls
    url(r'^get_claims/(?P<polygon_id>[\w.]{0,256})/$',
        claim_views.get_claims, name="get_claims"),
    url(r'^add_claim$', claim_views.add_claim, name="add_claim"),
]
