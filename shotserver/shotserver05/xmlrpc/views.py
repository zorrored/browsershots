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
        return xmlrpclib.dumps(xmlrpclib.Fault(404, str(error)))
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
