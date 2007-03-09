from django.conf.urls.defaults import *
from django.views.generic import list_detail
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser

urlpatterns = patterns('shotserver04.factories.views',
    (r'^$', 'factory_list'),
    (r'^(?P<factory_name>\S+)/$', 'factory_detail'),
)
