import sys
import xmlrpclib
from django.http import HttpResponse, Http404
from shotserver05.xmlrpc.utils import import_method


def dispatch_request(request):
    try:
        params, method_name = xmlrpclib.loads(request.raw_post_data)
    except expat.ExpatError, error:
        return xmlrpclib.dumps(
            xmlrpclib.Fault(400, u"XML parser error: " + str(error)))
    try:
        method = import_method(method_name)
        result = method(request, *params)
        response = (result, )
        return xmlrpclib.dumps(response, methodresponse=True)
    except Http404, error:
        return xmlprclib.dumps(xmlrpclib.Fault(404, str(error)))
    except xmlrpclib.Fault, fault:
        return xmlrpclib.dumps(fault)
    except:
        return xmlrpclib.dumps(
            xmlrpclib.Fault(500, u'%s: %s' % (sys.exc_type, sys.exc_value)))


def xmlrpc(request):
    try:
        is_post_request = len(request.POST)
    except (IOError, SystemError), error:
        return HttpResponse(str(error), status=500)
    if is_post_request:
        response = HttpResponse()
        response.write(dispatch_request(request))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        return HttpResponse("Please send a POST request for XML-RPC.")
