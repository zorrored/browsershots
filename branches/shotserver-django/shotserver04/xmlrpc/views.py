import sys
from django.http import HttpResponse
from shotserver04 import settings
from shotserver04.xmlrpc.dispatcher import Dispatcher


def xmlrpc(request):
    response = HttpResponse()
    if len(request.POST):
        response.write(dispatcher.dispatch_request(request))
    response['Content-length'] = str(len(response.content))
    return response


dispatcher = Dispatcher()
for app in settings.INSTALLED_APPS:
    try:
        module = __import__(app + '.xmlrpc', globals(), locals(), ['xmlrpc'])
    except ImportError:
        continue
    for name, item in module.__dict__.items():
        if callable(item):
            function_name = '%s.%s' % (app.split('.')[-1], name)
            dispatcher.register_function(item, function_name)
