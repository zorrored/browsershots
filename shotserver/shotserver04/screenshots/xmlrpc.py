# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
XML-RPC interface for screenshots app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
from xmlrpclib import Fault, Binary
from datetime import datetime
from shotserver04.common import serializable, get_or_fault
from shotserver04.xmlrpc import signature, factory_xmlrpc
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.requests.models import Request
from shotserver04.screenshots.models import Screenshot
from shotserver04.screenshots import storage

PREVIEW_SIZES = [512, 240, 160, 32]
# PREVIEW_SIZES = [512, 240, 160, 116, 92, 77, 57, 44, 32]
# PREVIEW_SIZES = [640, 316, 208, 154, 100, 64, 46]


@serializable
def close_request(request_id, factory, screenshot):
    """
    Close a screenshot request after it has been completed.
    """
    # Check again that no other factory has locked the request
    request = get_or_fault(Request, pk=request_id)
    try:
        request.check_factory_lock(factory)
    except Fault:
        screenshot.delete()
        raise
    # Close the request
    request.update_fields(screenshot_id=screenshot.id)


@factory_xmlrpc
@signature(str, str, str, int, Binary)
def upload(http_request, factory, encrypted_password, request, screenshot):
    """
    Submit a multi-page screenshot as a lossless PNG file.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)
    * encrypted_password string (lowercase hexadecimal, length 32)
    * request int (from requests.poll)
    * screenshot binary (BASE64-encoded PNG file)

    See nonces.verify for how to encrypt your password.

    Return value
    ~~~~~~~~~~~~
    * hashkey string (lowercase hexadecimal, length 32)

    Users can see the resulting uploaded screenshot at
    http://browsershots.org/screenshots/hashkey/
    """
    # Verify authentication
    nonces.verify(http_request, factory, encrypted_password)
    request_id = request
    request = get_or_fault(Request, pk=request_id)
    request_group = request.request_group
    # Make sure the request was locked by this factory
    request.check_factory_lock(factory)
    # Make sure the request was redirected by the browser
    browser = request.browser
    if browser is None or browser.factory != factory:
        raise Fault(406,
            u"The browser has not visited the requested website.")
    # Store and check screenshot file
    hashkey = storage.save_upload(screenshot)
    ppmname = storage.pngtoppm(hashkey)
    try:
        magic, width, height = storage.read_pnm_header(ppmname)
        if (request_group.width and request_group.width != width):
            raise Fault(412,
                u"The screenshot is %d pixels wide, not %d as requested." %
                (width, request_group.width))
        # Make smaller preview images
        for size in PREVIEW_SIZES:
            storage.scale(ppmname, size, hashkey)
    finally:
        # Delete temporary PPM file
        os.unlink(ppmname)
    # Save screenshot in database
    screenshot = Screenshot(hashkey=hashkey,
        user=request_group.user, website=request_group.website,
        factory=factory, browser=browser, width=width, height=height)
    screenshot.save()
    # Close the request
    close_request(request_id, factory, screenshot)
    # Update timestamps and estimates
    now = datetime.now()
    if request.priority == 0:
        factory.update_fields(last_upload=now,
            queue_estimate=(now - request_group.submitted).seconds)
    else:
        factory.update_fields(last_upload=now)
    browser.update_fields(last_upload=now)
    return hashkey
