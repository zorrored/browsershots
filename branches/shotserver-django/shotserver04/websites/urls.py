from django.conf.urls.defaults import *

urlpatterns = patterns('shotserver04.websites.views',
    (r'^$', 'website_list'),
)
