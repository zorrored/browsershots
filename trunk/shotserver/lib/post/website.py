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

def server_said(errornumber, errorstring, prefix = '', suffix = ''):
    result = "The server said '%d %s'." % (errornumber, errorstring)
    if prefix: result = prefix + ' ' + result
    if suffix: result = result + ' ' + suffix
    return result

def error_redirect(**params):
    location = '/?' + urllib.urlencode(params)
    util.redirect(req, location)

def sanity_check_url(url):
    protocol, server, path, query, fragment = urlparse.urlsplit(url, 'http')
    if protocol != 'http':
        raise error_redirect(error = "Protocol %s is not supported." % protocol, url = url)
    if not server:
        raise error_redirect(error = "Malformed URL. Please check for typos.", url = url)
    if not path:
        raise error_redirect(error = "There should be a slash after the server name. Please try again.", url = url + '/')

def test_head(url):
    protocol, server, path, query, fragment = urlparse.urlsplit(url, 'http')
    assert protocol == 'http'
    connection = httplib.HTTPConnection(server)
    try:
        if query: path += '?' + query
        connection.request('HEAD', path)
    except socket.error, (errornumber, errorstring):
        error_redirect(error = ' '.join(("Could not open web address.", errorstring + '.', "Please check for typos.")), url = url)
    response = connection.getresponse()
    if response.status == 302:
        redirected = response.getheader('Location')
        if fragment: redirected += '#' + fragment
        error_redirect(error = server_said(response.status, response.reason, "Your request has been redirected.", "Please try again."),
                       url = redirected)
    if response.status != 200:
        error_redirect(error = server_said(response.status, response.reason, "Unexpected server response."), url = url)

def redirect():
    url = read_form(req.info.form)
    sanity_check_url(url)
    test_head(url)
    website = select_or_insert(url)
    util.redirect(req, '/website/%d/' % website)
