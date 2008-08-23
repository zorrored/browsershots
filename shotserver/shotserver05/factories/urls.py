from django.conf.urls.defaults import *
from shotserver05.factories import views

urlpatterns = patterns('factories/',
    url(r'^$', views.index),
    url(r'^(?P<name>\S+)/$', views.details),
)
