# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Views for the xmlrpc app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import xmlrpclib
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from shotserver05.factories.models import Factory
from shotserver05.xmlrpc.utils import import_method


def dispatch_request(request):
    """
    Load the requested module and call XML-RPC method.
    """
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
        return xmlrpclib.dumps(xmlrpclib.Fault(404, str(error)))
    except xmlrpclib.Fault, fault:
        return xmlrpclib.dumps(fault)
    except:
        return xmlrpclib.dumps(
            xmlrpclib.Fault(500, u'%s: %s' % (sys.exc_type, sys.exc_value)))


def xmlrpc(request):
    """
    XML-RPC endpoint.
    """
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


def user_auth_html(request, username):
    """
    Get HTML file with encrypted user password for XML-RPC authentication.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user and username != 'testclient':
        return HttpResponseForbidden('Forbidden', 'text/plain')
    username = user.username
    password = user.password
    return render_to_response('xmlrpc/auth.html', locals(),
        context_instance=RequestContext(request))


def factory_auth_html(request, factory_name):
    """
    Get HTML file with secret key for XML-RPC authentication.
    """
    factory = get_object_or_404(Factory, name=factory_name)
    if request.user != factory.user and factory.user.username != 'testclient':
        return HttpResponseForbidden('Forbidden', 'text/plain')
    username = factory.name
    password = factory.secret_key
    return render_to_response('xmlrpc/auth.html', locals(),
        context_instance=RequestContext(request))
