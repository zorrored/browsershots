from django.conf.urls.defaults import patterns

urlpatterns = patterns('shotserver04.xmlrpc.views',
                       (r'^$', 'xmlrpc'),
                       (r'^(?P<method_name>[\w\.]+)/$', 'method_help'),
                       )
