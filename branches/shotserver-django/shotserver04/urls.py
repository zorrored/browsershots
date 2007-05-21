from django.conf.urls.defaults import *
from shotserver04 import settings


def load_app_patterns(prefix, ignore=()):
    pairs = []
    for app in settings.INSTALLED_APPS:
        if app.startswith(prefix):
            segment = app.split('.')[-1]
            if segment not in ignore:
                pairs.append((r'^%s/' % segment, include(app + '.urls')))
    return pairs


urlpatterns = patterns('',
    (r'^$', 'shotserver04.common.views.start'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^(?P<website_url>https?://\S+)$',
         'shotserver04.websites.views.website_detail'),
    *load_app_patterns('shotserver04.', ignore=['common']))

if settings.DEBUG:
    import os
    local_path = os.path.normpath(os.path.dirname(__file__))
    static_path = os.path.join(local_path, 'common', 'static')
    # Serve CSS and image files from common/static
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': static_path}),
        )
