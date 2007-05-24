from django.conf.urls.defaults import *

urlpatterns = patterns('shotserver04.screenshots.views',
    (r'^$', 'screenshot_list'),
)
