from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^factories/', include('shotserver04.factories.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)
