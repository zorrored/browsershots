from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^shotserver04/', include('shotserver04.foo.urls')),
    (r'^admin/', include('django.contrib.admin.urls')),
)
