from django.conf.urls.defaults import *

urlpatterns = patterns('shotserver04.factories.views',
    (r'^$', 'index'),
    (r'^(?P<factory_name>\S+)/$', 'details'),
)
