from django.conf.urls.defaults import *
from django.views.generic import list_detail
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser

factory_list_info = {
    'queryset': Factory.objects.all(),
    'allow_empty': True,
    'paginate_by': 10,
    }

urlpatterns = patterns('',
    (r'^$', list_detail.object_list, factory_list_info),
    (r'^page(?P<page>\d+)/$', list_detail.object_list, factory_list_info),
    (r'^(?P<factory_name>\S+)/$',
     'shotserver04.factories.views.factory_detail'),
)
