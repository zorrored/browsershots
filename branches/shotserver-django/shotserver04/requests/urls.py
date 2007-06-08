from django.conf.urls.defaults import patterns

urlpatterns = patterns('shotserver04.requests.views',
    (r'^$', 'request_list'),
)
