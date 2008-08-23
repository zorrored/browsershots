from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^factories/', include('shotserver05.factories.urls')),
    (r'^xmlrpc/', include('shotserver05.xmlrpc.urls')),
    (r'^admin/(.*)', admin.site.root),
)
