# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Self-documenting XML-RPC interface.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from shotserver04 import settings
from shotserver04.xmlrpc.dispatcher import Dispatcher

RST_SETTINGS = {
    'initial_header_level': 2,
    'doctitle_xform': False,
    'docinfo_xform': False,
    }


def xmlrpc(request):
    """
    XML-RPC interface (for POST requests) and automatic human-readable
    HTML documentation (for GET requests).
    """
    if len(request.POST):
        response = HttpResponse()
        response.write(dispatcher.dispatch_request(request))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        method_list = dispatcher.list_methods(request)
        return render_to_response('xmlrpc/method_list.html', locals())


def method_help(request, method_name):
    """
    Display automatic help about an XML-RPC method.
    """
    if len(request.POST):
        raise Http404 # Don't POST here, only GET documentation
    if method_name not in dispatcher.list_methods(request):
        raise Http404 # Method not found
    signatures = dispatcher.method_signature(request, method_name)
    signature_lines = []
    for signature in signatures:
        result = signature[0]
        params = signature[1:]
        signature_lines.append('%s(%s) => %s' % (
            method_name, ', '.join(params), result))
    docstring = dispatcher.method_help(request, method_name)
    try:
        from docutils import core
        parts = core.publish_parts(
            source=docstring, writer_name='html',
            settings_overrides=RST_SETTINGS)
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
