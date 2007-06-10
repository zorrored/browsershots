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
Redirect the browser to the requested URL for each screenshot.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from xmlrpclib import Fault
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from shotserver04.browsers.models import Browser
from datetime import datetime


def redirect(http_request, factory_name, encrypted_password, request_id):
    try:
        factory = get_object_or_404(Factory, name=factory_name)
        nonces.verify(http_request, factory, encrypted_password)
        request = get_object_or_404(Request, id=request_id)
        request.check_factory_lock(factory)
        user_agent = http_request.META['HTTP_USER_AGENT']
        try:
            browser = Browser.objects.get(
                factory=factory, user_agent=user_agent)
        except Browser.DoesNotExist:
            raise Fault(0, "Unknown user agent: %s." % user_agent)
        request.browser = browser
        request.redirected = datetime.now()
        request.save()
        website = request.request_group.website
        return HttpResponseRedirect(website.url)
    except Fault, fault:
        return render_to_response('redirect/error.html',
                                  {'message': fault.faultString})
