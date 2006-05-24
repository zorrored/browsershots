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
Insert a new website into the database.
"""

__revision__ = '$Rev: 117 $'
__date__ = '$Date: 2006-04-08 08:51:18 +0200 (Sat, 08 Apr 2006) $'
__author__ = '$Author: johann $'

import re, httplib, urllib, urlparse, socket
from mod_python import util
from shotserver03.interface import xhtml
from shotserver03 import database

class InvalidURLError(Exception):
    pass

def read_form(form):
    url = ''
    for key in form.keys():
        if key == 'url':
            url = form[key]
        elif key == 'submit':
            pass
        else:
            raise "unexpected input: %s" % key
    return url

def select_or_insert(url):
    """
    Get the website id of a URL. Insert URL into website table if necessary.
    """
    database.connect()
    try:
        cur.execute("SELECT website FROM website WHERE url=%s", url)
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO website (url) VALUES (%s)", url)
            cur.execute("SELECT website FROM website WHERE url=%s", url)
            row = cur.fetchone()
        return row['website']
    finally:
        database.disconnect()

def ucfirst(s):
    return s[0].upper() + s[1:]

def server_said(errornumber, errorstring, prefix = '', suffix = ''):
    errorstring = ucfirst(errorstring)
    result = "The server said '%d %s'." % (errornumber, errorstring)
    if prefix: result = prefix + ' ' + result
    if suffix: result = result + ' ' + suffix
    return result

def error_redirect(**params):
    params = urllib.urlencode(params)
    if params:
        util.redirect(req, '/?' + params)
    else:
        util.redirect(req, '/')

port_match = re.compile(r':(\d+)$').search
def get_port(protocol, server):
    match = port_match(server)
    if match:
        return int(match.group(1))
    elif protocol == 'http':
        return 80
    elif protocol == 'https':
        return 443
    else:
        raise "Protocol %s is not supported." % protocol

def sanity_check_url(url):
    if not url:
        error_redirect()

    protocol, server, path, query, fragment = urlparse.urlsplit(url, '')
    if not protocol:
        if not url.count('/'):
            url += '/'
        suggestion = 'http://' + url.lstrip('/')
        raise error_redirect(error = "URL must start with 'http://' or 'https://'. Please try again.", url = suggestion)

    if protocol not in ('http', 'https'):
        raise error_redirect(error = "Protocol %s is not supported." % protocol, url = url)
    if not server:
        raise error_redirect(error = "Malformed URL. Please check for typos.", url = url)

    port = get_port(protocol, server)
    if port == 80:
        if protocol != 'http':
            raise error_redirect(error = "Protocol must be http on port 80.", url = url)
    elif port == 443:
        if protocol != 'https':
            raise error_redirect(error = "Protocol must be https on port 443.", url = url)
    elif port < 1024:
        raise error_redirect(error = "Port %d is not supported." % port, url = url)

    if not path:
        raise error_redirect(error = "There must be a slash after the server name. Please try again.", url = url + '/')

def test_head(url):
    protocol, server, path, query, fragment = urlparse.urlsplit(url, '')
    try:
        if protocol == 'http':
            connection = httplib.HTTPConnection(server)
        elif protocol == 'https':
            connection = httplib.HTTPSConnection(server)
        else:
            raise "Protocol %s is not supported." % protocol
    except httplib.HTTPException, e:
        error_redirect(error = ' '.join(("Could not open web address.", ucfirst(str(e)) + '.', "Please check for typos.")), url = url)

    if query: path += '?' + query
    try:
        connection.request('HEAD', path)
    except socket.error, (errornumber, errorstring):
        error_redirect(error = ' '.join(("Could not open web address.", errorstring + '.', "Please check for typos.")), url = url)

    response = connection.getresponse()
    if response.status == 200:
        pass # all good
    elif response.status in (301, 302):
        redirected = response.getheader('Location')
        if fragment: redirected += '#' + fragment
        error_redirect(error = server_said(response.status, response.reason, "Your request has been redirected.", "Please try again."), url = redirected)
    else:
        error_redirect(error = server_said(response.status, response.reason, "Unexpected server response."), url = url)

def redirect():
    url = read_form(req.info.form)
    sanity_check_url(url)
    test_head(url)
    website = select_or_insert(url)
    util.redirect(req, '/website/%d/' % website)
