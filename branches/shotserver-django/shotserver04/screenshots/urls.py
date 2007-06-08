from django.conf.urls.defaults import patterns

urlpatterns = patterns('shotserver04.screenshots.views',
    (r'^$', 'screenshot_list'),
)
