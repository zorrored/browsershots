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
Custom URL rewriting, more granular than Django's APPEND_SLASH.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.conf import settings
from django import http


class RedirectMiddleware(object):
    """
    Append missing slashes, but only if path starts with the name of
    an installed app. Special URLs like this will be left untouched::

      http://browsershots.org/http://www.example.com/no-slash

    Also redirect to XML-RPC documentation if subdomain is 'api' or
    'xmlrpc' and path is '/'.
    """

    def process_request(self, request):
        """
        Process an incoming HTTP GET or HEAD request.
        """
        # Don't rewrite POST requests
        if not request.method in ('GET', 'HEAD'):
            return
        first_part = request.path.strip('/').split('/')[0]
        # Redirect to XML-RPC documentation
        host = http.get_host(request)
        subdomain = host.lower().split('.')[0]
        if subdomain in ('api', 'xmlrpc') and first_part == '':
            return http.HttpResponsePermanentRedirect('/xmlrpc/')
        # Add trailing slash if path starts with an installed app name
        if self.installed_app(first_part) and not request.path.endswith('/'):
            new_path = request.path + '/'
            if request.GET:
                new_path += '?' + request.GET.urlencode()
            return http.HttpResponsePermanentRedirect(new_path)

    def installed_app(self, name):
        """
        Check if this is the name of an installed app.
        """
        name = '.' + name
        for app in settings.INSTALLED_APPS:
            if app.endswith(name):
                return True
