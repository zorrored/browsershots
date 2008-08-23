from django.conf.urls.defaults import *
from shotserver05.xmlrpc import views

urlpatterns = patterns('xmlrpc/',
    url(r'^$', views.xmlrpc),
)
