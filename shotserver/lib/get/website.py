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
Show a website overview.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

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
                raise InvalidParameters("The web address seems to be invalid (%s)." % url)
            website = database.website.select_serial(url)
        if not url:
            raise InvalidParameters("Web address parameter is missing.")
        req.params.website = website
        req.params.url = url
        req.params.simple = simple_url_match(url)
        req.params.escaped = cgi.escape(url, quote = True)
        req.params.show_screenshots = database.screenshot.select_recent(req.params.website)
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
        return "Recent screenshots"
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

    xhtml.write_tag_line('p', 'for ' + req.params.url, _class="up")

    if req.params.show_screenshots:
        screenshots.write()

    if req.params.show_queue:
        if req.params.show_screenshots:
            xhtml.write_tag_line('h2', "Request queue")
        queue.write()

    if req.params.show_screenshots or req.params.show_queue:
        xhtml.write_tag_line('h2', "Select browsers and configuration")

    xhtml.write_open_tag_line('form', action="/submitjobs/", method="post")

    xhtml.write_open_tag('div')
    xhtml.write_tag('input', _type="hidden", _name="url", value=req.params.escaped)
    xhtml.write_close_tag_line('div')

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
