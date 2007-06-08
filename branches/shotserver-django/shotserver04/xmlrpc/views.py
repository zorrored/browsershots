from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from shotserver04 import settings
from shotserver04.xmlrpc.dispatcher import Dispatcher

rst_settings = {
    'initial_header_level': 2,
    'doctitle_xform': False,
    'docinfo_xform': False,
    }


def xmlrpc(request):
    if len(request.POST):
        response = HttpResponse()
        response.write(dispatcher.dispatch_request(request))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        method_list = dispatcher.system_listMethods(request)
        return render_to_response('xmlrpc/method_list.html', locals())


def method_help(request, method_name):
    if len(request.POST):
        raise Http404 # Don't POST here, only GET documentation
    if method_name not in dispatcher.system_listMethods(request):
        raise Http404 # Method not found
    signatures = dispatcher.system_methodSignature(request, method_name)
    signature_lines = []
    for signature in signatures:
        result = signature[0]
        params = signature[1:]
        signature_lines.append('%s(%s) => %s' % (
            method_name, ', '.join(params), result))
    docstring = dispatcher.system_methodHelp(request, method_name)
    try:
        from docutils import core
        parts = core.publish_parts(
            source=docstring, writer_name='html',
            settings_overrides=rst_settings)
        docstring = parts['html_body']
    except ImportError:
        docstring = '<pre>\n%s\n</pre>\n' % docstring
    for method in dispatcher.funcs:
        docstring = docstring.replace(
            method, '<a href="../%s/">%s</a>' % (method, method))
    return render_to_response('xmlrpc/method_help.html', locals())


dispatcher = Dispatcher()
for app in settings.INSTALLED_APPS:
    try:
        module = __import__(app + '.xmlrpc', globals(), locals(), ['xmlrpc'])
    except ImportError:
        continue
    for name, item in module.__dict__.items():
        if hasattr(item, '_signature'):
            function_name = '%s.%s' % (app.split('.')[-1], name)
            dispatcher.register_function(item, function_name)
