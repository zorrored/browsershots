from django.conf.urls.defaults import patterns

urlpatterns = patterns('shotserver04.websites.views',
    (r'^$', 'website_list'),
    (r'^(?P<website_id>\d+)/$', 'website_numeric'),
)
