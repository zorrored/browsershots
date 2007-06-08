from django.conf.urls.defaults import patterns

urlpatterns = patterns('shotserver04.factories.views',
    (r'^$', 'factory_list'),
    (r'^(?P<factory_name>\S+)/$', 'factory_detail'),
)
