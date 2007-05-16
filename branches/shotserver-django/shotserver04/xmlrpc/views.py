from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse

# dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)
dispatcher = SimpleXMLRPCDispatcher()
dispatcher.register_introspection_functions()


def xmlrpc(request):
    response = HttpResponse()
    if len(request.POST):
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    response['Content-length'] = str(len(response.content))
    return response
