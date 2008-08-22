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
Show a website overview.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import cgi
from mod_python import util
from shotserver03.interface import xhtml
from shotserver03.segments import screenshots, queue, browsers
from shotserver03.segments import features # , queue_notice
from shotserver03 import database

request_match = re.compile(
    r'(\w+)\s+(/(|intl/[\w\-]+/)website/(\S*))\s+(HTTP/[\d\.]+)$').match
simple_url_match = re.compile(r'^(https?://[\w\.,:;\-\_/\?&=%\[\]]+)$').match
protocol_match = re.compile(r'^(\w+:)(/+)(.+)$').match


class InvalidParameters(Exception):
    """The HTTP GET request is invalid."""
    pass


def request_is_numeric():
    """
    Check if the request URI is of the form /website/<decimal>/.
    """
    if len(req.info.options) != 1:
        return False
    return req.info.options[0].isdigit()


def double_slash(url):
    """
    Make sure that the URL has a double slash.
    """
    match = protocol_match(url)
    if match:
        protocol, slashes, rest = match.groups()
        if slashes != '//':
            url = protocol + '//' + rest
    return url


def read_params():
    """
    Read parameters from the request URL.
    """
    req.params.website = None
    req.params.url = None
    req.params.simple = None
    req.params.escaped = None
    req.params.show_screenshots = None
    req.params.show_queue = None

    website = None
    url = None
    database.connect()
    try:
        if request_is_numeric():
            website = int(req.info.options[0])
            url = database.website.select_url(website)
        else:
            match = request_match(req.the_request)
            if not match:
                raise InvalidParameters(
                    "Your browser sent a strange request (%s)." %
                    req.the_request)
            url = double_slash(match.group(4))
            match = simple_url_match(url)
            if url and not match:
                raise InvalidParameters(
                    "The web address seems to be invalid (%s)." % url)
            website = database.website.select_serial(url)
        req.params.website = website
        if website:
            req.params.show_screenshots = database.screenshot.select_recent(
                'website = %s', (website, ))
            req.params.show_queue = database.request.select_by_website(website)
        req.params.url = url
        if url:
            req.params.simple = simple_url_match(url)
            req.params.escaped = cgi.escape(url, quote = True)
            req.params.linkable = url.replace('?', '%3F').replace('&', '%26')
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
    elif req.params.url and req.params.website:
        return "Select browsers and configuration"
    else:
        return "Unknown web address"


def body():
    """
    Write XHTML body content.
    """
    #link = xhtml.tag('a', url, href=escaped, _class="ext-link")
    #xhtml.write_tag_line('p', link, _class="center bold")

    if req.params.url:
        bold = xhtml.tag('b', 'for ' + req.params.escaped)
        xhtml.write_tag_line('p', bold, _class="up")
    else:
        return

    if not req.params.website:
        xhtml.write_tag_line('p', '<br />\n'.join((
            "The requested web address was not found in the database.",
            xhtml.tag('a', "Please go to the start page to register it first.",
                      href="/?url=%s" % req.params.linkable),
            )))
        return

    # queue_notice.write()

    if req.params.show_screenshots and req.params.show_queue:
        xhtml.write_tag_line('p', '<br />\n'.join((
"This page shows the screenshots and requests for a single web address.",
"You can bookmark this page to check for new screenshots later.")))
    elif req.params.show_screenshots:
        xhtml.write_tag_line('p', '<br />\n'.join((
"This page shows the newest screenshots for a single web address.",
"You can bookmark this page to check for new screenshots later.")))
    elif req.params.show_queue:
        xhtml.write_tag_line('p', '<br />\n'.join((
"This page shows queued requests for a single web address.",
"When the first screenshots are uploaded, they will appear here too.",
"You can bookmark this page to check for screenshots later.")))

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
    xhtml.write_tag('input', _type="hidden", _name="url",
                    value=req.params.escaped)
    xhtml.write_close_tag_line('div')

    browsers.write()
    features.write()
    xhtml.write_close_tag_line('form')

    xhtml.write_tag_line('h2', "What is this?")
    xhtml.write_tag_line('p', '\n'.join((
"On this page you can choose browser configurations for your screenshots.",
"Select your preferred browsers above.",
"The drop-down boxes let you request special features.")))
    xhtml.write_tag_line('p', '\n'.join((
"When you click the submit button, your requests will be added to the queue.",
"It will take a while before your screenshots will be uploaded.",
"Some features are not available for all browsers.",
"Unprocessed screenshots requests will expire after your maximum wait.")))
