import os
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^factories/', include('shotserver05.factories.urls')),
    (r'^users/', include('shotserver05.users.urls')),
    (r'^xmlrpc/', include('shotserver05.xmlrpc.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    # Serve CSS and image files from shotserver04/static/
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.normpath(
                        os.path.dirname(__file__)), 'static')}),
#        (r'^png/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.PNG_ROOT}),
        )
