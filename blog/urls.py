from django.conf.urls import url

from blog import views

urlpatterns = [

    url(r'^$', views.entry_list),
    url(r'^add$', views.entry_add),
    url(r'^(?P<post_id>[0-9]+)/$', views.entry),

]
