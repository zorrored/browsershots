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
Insert a new website into the database.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import httplib
import urllib
import urlparse
import socket
from mod_python import util
from shotserver03 import database


class UnexpectedInput(Exception):
    """Post form input had unexpected fields."""
    pass


class UnsupportedProtocol(Exception):
    """The specified web address didn't start with http:// or https://."""
    pass


def read_form(form):
    """
    Get known fields from post form.
    Raise UnexpectedInput if field name is not known.
    """
    url = ''
    for key in form.keys():
        if key == 'url':
            url = form[key]
        elif key == 'submit':
            pass
        else:
            raise UnexpectedInput(key)
    return url


def server_said(errornumber, errorstring, prefix = '', suffix = ''):
    """
    Return a human-readable error message with the server answer.
    """
    errorstring = errorstring.capitalize()
    result = "The server said '%d %s'." % (errornumber, errorstring)
    if prefix:
        result = prefix + ' ' + result
    if suffix:
        result = result + ' ' + suffix
    return result


def error_redirect(**params):
    """
    Redirect back to front page because an error has occurred.
    """
    params = urllib.urlencode(params)
    if params:
        util.redirect(req, '/?' + params)
    else:
        util.redirect(req, '/')


port_match = re.compile(r':(\d+)$').search


def get_port(protocol, server):
    """
    Extract the port number from the server part of the URL.
    """
    match = port_match(server)
    if match:
        return int(match.group(1))
    elif protocol == 'http':
        return 80
    elif protocol == 'https':
        return 443
    else:
        raise UnsupportedProtocol(protocol)


def sanity_check_url(url):
    """
    Check the URL for obvious errors.
    """
    if not url:
        error_redirect()

    protocol, server, path, dummy, dummy = urlparse.urlsplit(url, '')
    if not protocol:
        if not url.count('/'):
            url += '/'
        suggestion = 'http://' + url.lstrip('/')
        error_redirect(error=' '.join((
            "URL must start with 'http://' or 'https://'.",
            "Please try again.")), url=suggestion)

    if protocol not in ('http', 'https'):
        error_redirect(error="Protocol %s is not supported." % protocol,
                       url=url)
    if not server:
        error_redirect(error="Malformed URL. Please check for typos.", url=url)

    port = get_port(protocol, server)
    if port == 80:
        if protocol != 'http':
            error_redirect(error="Protocol must be http on port 80.", url=url)
    elif port == 443:
        if protocol != 'https':
            error_redirect(error="Protocol must be https on port 443.",
                           url=url)
    elif port < 1024:
        error_redirect(error="Port %d is not supported." % port, url=url)

    if not path:
        error_redirect(error=' '.join((
            "There must be a slash after the server name.",
            "Please try again.")), url=url + '/')


def test_get(url):
    """
    Test the URL with a GET request.
    If unsuccessful, redirect back to front page with error message.
    """
    socket.setdefaulttimeout(10)
    protocol, server, path, query, fragment = urlparse.urlsplit(url, '')
    try:
        if protocol == 'http':
            connection = httplib.HTTPConnection(server)
        elif protocol == 'https':
            connection = httplib.HTTPSConnection(server)
        else:
            raise UnsupportedProtocol(protocol)
    except httplib.HTTPException, error:
        error = ' '.join(("Could not open web address.",
                          str(error).capitalize() + '.',
                          "Please check for typos."))
        error_redirect(error = error, url = url)

    if query:
        path += '?' + query
    try:
        headers = {"User-Agent": "Browsershots URL Check"}
        connection.request('GET', path, headers=headers)
    except socket.error, error:
        try:
            (dummy, errorstring) = error.args
        except ValueError:
            errorstring = str(error)
        if errorstring:
            errorstring = errorstring[0].upper() + errorstring[1:]
        error = ' '.join((
            "Could not open web address.",
            errorstring + '.',
            "Please check for typos."))
        error_redirect(error = error, url = url)

    try:
        response = connection.getresponse()
    except socket.timeout:
        error = ' '.join(("Timeout on server (%s)." % server,
                          "Please try again later."))
        error_redirect(error = error, url = url)

    try:
        if response.status == 200:
            pass # all good
        elif response.status in (301, 302, 303, 307):
            redirected = response.getheader('Location')
            if redirected is None:
                error = server_said(response.status, response.reason,
                                    "Your request has been redirected, " +
                                    "but no location was specified.")
                error_redirect(error = error, url = url)
            if redirected.startswith('/'):
                redirected = '%s://%s%s' % (protocol, server, redirected)
            if fragment:
                redirected += '#' + fragment
            error = server_said(response.status, response.reason,
                                "Your request has been redirected.",
                                "Please try again.")
            error_redirect(error = error, url = redirected)
        else:
            error = server_said(response.status, response.reason,
                                "Unexpected server response.")
            error_redirect(error = error, url = url)
    finally:
        connection.close()


def redirect():
    """
    Insert URL into database.
    Redirect to overview page on success.
    Redirect back to front page on error.
    """
    url = read_form(req.info.form)
    sanity_check_url(url)
    test_get(url)

    database.connect()
    try:
        website = database.website.select_serial(url, insert = True)
    finally:
        database.disconnect()

    util.redirect(req, '/website/%d/' % website)
