from django.conf.urls.defaults import *
from shotserver05.users import views

urlpatterns = patterns('users/',
    url(r'^register/$', views.register),
    url(r'^validate/(\S+)/$', views.validate),
)
