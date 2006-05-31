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

import re, cgi
from mod_python import util
from shotserver03.interface import xhtml
from shotserver03.segments import screenshots, queue, browsers, features
from shotserver03 import database

class InvalidParameters(Exception):
    """The HTTP GET request is invalid."""
    pass

request_match = re.compile(r'(\w+)\s+(/(|intl/[\w\-]+/)website/(\S*))\s+(HTTP/[\d\.]+)$').match
simple_url_match = re.compile(r'^(https?://[\w\.,:;\-\_/\?&=%]+)$').match

def request_is_numeric():
    """
    Check if the request URI is of the form /website/<decimal>/.
    """
    if len(req.info.options) != 1:
        return False
    return req.info.options[0].isdigit()

def read_params():
    """
    Read parameters from the request URL.
    """
    database.connect()
    try:
        if request_is_numeric():
            website = int(req.info.options[0])
            url = database.website.select_url(website)
        else:
            match = request_match(req.the_request)
            if not match:
                raise InvalidParameters("Your browser sent a strange request (%s)." % req.the_request)
            url = match.group(4)
            match = simple_url_match(url)
            if url and not match:
                return InvalidParameters("The web address seems to be invalid (%s)." % url)
            website = database.website.select_serial(url)
        if url is None:
            return InvalidParameters("Web address parameter is missing.")
        req.params.website = website
        req.params.url = url
        req.params.simple = simple_url_match(url)
        req.params.escaped = cgi.escape(url, quote = True)
        req.params.show_screenshots = False
        req.params.show_queue = database.request.select_by_website(website)
    finally:
        database.disconnect()

def redirect():
    """
    Redirect if the website address can be shown in the URL.
    """
    if not request_is_numeric():
        return False
    if not req.params.simple:
        return False
    location = 'http://%s/website/%s' % (req.info.uri.hostname, req.params.url)
    util.redirect(req, location)

def title():
    """
    Page title.
    """
    if req.params.show_screenshots:
        return "Screenshots"
    elif req.params.show_queue:
        return "Request queue"
    else:
        return "Select browsers and configuration"

def body():
    """
    Write XHTML body content.
    """
    #link = xhtml.tag('a', url, href=escaped, _class="ext-link")
    #xhtml.write_tag_line('p', link, _class="center bold")

    # explain = "This page will show screenshots for the web address above when they get uploaded."
    # bookmark = "To come back later, bookmark this page or simply enter the address on the front page again."
    # xhtml.write_tag_line('p', '<br />\n'.join((explain, bookmark)))

    if req.params.show_screenshots:
        screenshots.write()

    if req.params.show_queue:
        queue.write()

    if req.params.show_screenshots or req.params.show_queue:
        xhtml.write_tag_line('h2', "Select browsers and configuration")

    xhtml.write_open_tag_line('form', action="/submitjobs/", method="post")
    xhtml.write_tag_line('input', _type="hidden", _name="url", value=req.params.escaped)
    browsers.write()
    features.write()
    xhtml.write_close_tag_line('form')

    xhtml.write_tag_line('h2', "What is this?")
    xhtml.write_tag_line('p', '\n'.join((
        "On this page you can choose browser configurations for your screenshots.",
        "At the top, select the browsers that you're interested in.",
        "The drop-down boxes let you request special features.")))
    xhtml.write_tag_line('p', '\n'.join((
        "When you click the submit button, your screenshot requests will be added to the queue.",
        "It will take a while before your screenshots will be uploaded, depending on the length of the queue.",
        "Some feature combinations are impossible.",
        "If some of your requests can't be finished within your maximum wait, they will be ignored.")))
