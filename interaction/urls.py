from django.conf.urls import url

from interaction import views

urlpatterns = [

    url(r'^(?P<user_id>[0-9]+)/$', views.profile),
]
