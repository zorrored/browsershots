# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from mod_python import util
from shotserver03.interface import xhtml
from shotserver03 import database

def redirect():
    """
    Save the user-agent string, then redirect to the request URL.
    """
    database.connect()
    try:
        row = database.nonce.authenticate_redirect(req.info.options[0])
        status, url, request, request_group, request_name, request_major, request_minor = row
        if status == 'OK':
            user_agent = req.headers_in.get('User-Agent', '')
            row = database.browser.select_by_user_agent(user_agent)
            if row is None:
                req.params.status = "Your browser version is not registered."
                req.params.extra = user_agent
                return
            browser, group, name, major, minor = row
            if ((request_group is not None and group != request_group) or
                (request_major is not None and major != request_major) or
                (request_minor is not None and minor != request_minor)):
                req.params.status = "Browser mismatch."
                req.params.extra = "Expected %s, got %s." % (
                    database.browser.version_string(request_name, request_major, request_minor),
                    database.browser.version_string(name, major, minor))
                return
            database.request.update_browser(request, browser)
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
