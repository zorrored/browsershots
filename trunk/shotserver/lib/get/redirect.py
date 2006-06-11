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
        ip = req.connection.remote_ip
        crypt = req.info.options[0]
        status, url, request = database.nonce.authenticate_redirect(ip, crypt)
        if status == 'OK':
            header = req.headers_in.get('User-Agent', '')
            useragent = database.useragent.select_serial(header, insert=True)
            database.request.update_useragent(request, useragent)
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
