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
XML-RPC interface for screenshots app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from xmlrpclib import Fault, Binary
from datetime import datetime
from shotserver04.common import serializable, get_or_fault
from shotserver04.xmlrpc import register
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from shotserver04.screenshots.models import Screenshot
from shotserver04.screenshots import storage

PREVIEW_SIZES = [512, 240, 160, 116, 92, 77, 57, 44, 32]
# PREVIEW_SIZES = [640, 316, 208, 154, 100, 64, 46]


@serializable
def close_request(request_id, factory, browser, screenshot):
    # Check again that no other factory has locked the request
    request = get_or_fault(Request, pk=request_id)
    try:
        request.check_factory_lock(factory)
    except Fault:
        screenshot.delete()
        raise
    # Close the request
    now = datetime.now()
    request.uploaded = now
    request.save()
    factory.last_upload = now
    factory.save()
    browser.last_upload = now
    browser.queue_estimate = (now - request.request_group.submitted).seconds
    browser.save()


@register(None, str, str, int, Binary)
def upload(http_request,
           factory_name, encrypted_password, request, screenshot):
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
    http://browsershots.org/screenshots/<hashkey>/
    """
    # Verify authentication
    factory = get_or_fault(Factory, name=factory_name)
    nonces.verify(http_request, factory, encrypted_password)
    request_id = request
    request = get_or_fault(Request, pk=request_id)
    # Make sure the request was locked by this factory
    request.check_factory_lock(factory)
    # Make sure the request was redirected by the browser
    browser = request.browser
    if browser is None:
        raise Fault(0,
            "The browser has not visited the requested website.")
    # Store and check screenshot file
    hashkey = storage.save_upload(screenshot)
    ppmname = storage.pngtoppm(hashkey)
    magic, width, height = storage.read_pnm_header(ppmname)
    # Make smaller preview images
    for size in PREVIEW_SIZES:
        storage.scale(ppmname, size, hashkey)
    # Save screenshot in database
    screenshot = Screenshot(
        factory=factory, browser=browser, request=request,
        hashkey=hashkey, width=width, height=height)
    screenshot.save()
    # Close request and update timestamps in database
    close_request(request_id, factory, browser, screenshot)
    return hashkey
