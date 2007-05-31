from django.conf.urls.defaults import *

urlpatterns = patterns('shotserver04.redirect.views',
    (r'^$', 'redirect_help'),
    (r'^(?P<factory_name>\S+)' +
     r'/(?P<encrypted_password>\w+)' +
     r'/(?P<request_id>\d+)' +
     r'/$', 'redirect'),
)
