# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        row = database.nonce.authenticate_redirect(req.connection.remote_ip, req.info.options[0])
        status, url, request, request_group, request_name, request_major, request_minor = row
        if status == 'OK':
            useragent = req.headers_in.get('User-Agent', '')
            row = database.browser.select_by_useragent(useragent)
            if row is None:
                req.params.status = "Your browser version is not registered."
                req.params.extra = useragent
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
