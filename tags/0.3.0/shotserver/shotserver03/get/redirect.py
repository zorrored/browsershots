# browsershots.org ShotServer 0.3-beta1
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
Redirect a screenshot factory browser and save the user-agent string.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
from mod_python import util
from shotserver03.interface import xhtml
from shotserver03 import database

timeout = 10 # seconds


def redirect():
    """
    Save the user-agent string, then redirect to the request URL.
    """
    start = time.time()
    database.connect()
    try:
        crypt = req.info.options[0]
        if len(req.info.options) > 1 and req.info.options[1].isdigit():
            request = int(req.info.options[1])
            row = database.nonce.authenticate_redirect(crypt, request)
        else:
            row = database.nonce.authenticate_redirect(crypt)
        (status, url,
         request, request_name, request_major, request_minor,
         factory) = row
        if status == 'OK':
            user_agent = req.headers_in.get('User-Agent', '')
            row = database.browser.select_by_user_agent(factory, user_agent)
            if row is None:
                req.params.status = "Your browser version is not registered."
                req.params.extra = user_agent
                return
            factory_browser, name, major, minor = row
            if ((request_name is not None and name != request_name) or
                (request_major is not None and major != request_major) or
                (request_minor is not None and minor != request_minor)):
                req.params.status = "Browser mismatch."
                expected = database.browser.version_string(
                        request_name, request_major, request_minor)
                actual = database.browser.version_string(name, major, minor)
                req.params.extra = "Expected %s, got %s." % (expected, actual)
                return
            database.request.update_browser(request, factory_browser)
            if time.time() - start > timeout:
                req.params.status = "Sorry, the server load is too high."
                req.params.extra = "Redirect took more than %s seconds."
                req.params.extra %= timeout
                return
            util.redirect(req, url)
        else:
            req.params.status = status
    finally:
        database.disconnect()


def title():
    """Page title."""
    return "Redirect Error"


def body():
    """Print error message."""
    xhtml.write_tag('p', req.params.status, _class="error")
    if hasattr(req.params, 'extra'):
        xhtml.write_tag('p', req.params.extra)
