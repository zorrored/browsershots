from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^factories/$', 'shotserver04.factories.views.index'),
    (r'^admin/', include('django.contrib.admin.urls')),
)
