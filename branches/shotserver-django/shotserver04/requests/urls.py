from django.conf.urls.defaults import *

urlpatterns = patterns('shotserver04.requests.views',
    (r'^$', 'request_list'),
)
