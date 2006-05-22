# -*- coding: utf-8 -*-
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
Show a website overview.
"""

__revision__ = '$Rev: 117 $'
__date__ = '$Date: 2006-04-08 08:51:18 +0200 (Sat, 08 Apr 2006) $'
__author__ = '$Author: johann $'

import re
from mod_python import util
from shotserver03.interface import xhtml
from shotserver03 import database

def request_is_numeric():
    if len(req.info.options) != 1:
        return False
    return req.info.options[0].isdigit()

def request_numeric_to_int():
    return int(req.info.options[0])

def request_numeric_to_url():
    request_int = request_numeric_to_int()
    database.connect()
    try:
        cur.execute("SELECT url FROM website WHERE website = %s", request_int)
        result = cur.fetchone()
    finally:
        database.disconnect()
    if result is None:
        return None
    return result['url']

simple_url_match = re.compile(r'^(\w+://\w[\w\.\-\_/]+\w/?)$').match
def redirect():
    """
    Redirect if the website address can be shown in the URL.
    """
    if not request_is_numeric():
        return False

    url = request_numeric_to_url()
    if url is None:
        return False

    match = simple_url_match(url)
    if match is None:
        return False

    location = 'http://%s/website/%s' % (req.info.uri.hostname, url)
    util.redirect(req, location)

def title():
    return "Website"

request_match = re.compile(r'(\w+)\s+/website/(\S*)\s+(HTTP/[\d\.]+)$').match
def body():
    if request_is_numeric():
        website = request_numeric_to_url()
    else:
        match = request_match(req.the_request)
        if match is None:
            raise "Request does not match: %s" % req.the_request
        website = match.group(2)

    xhtml.write_open_tag_line('div')
    if not website:
        xhtml.write_tag_line('p', "Unknown website.", _class="error")
    else:
        website = website.replace('&', '&amp;')
        xhtml.write_tag_line('p', website)
    xhtml.write_close_tag_line('div')
