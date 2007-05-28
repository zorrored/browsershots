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
Show a user's factories.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from mod_python import util
from shotserver03.segments import factory_list
from shotserver03 import database


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


def read_params():
    """
    Read parameters from the request URL.
    """
    req.params.person = None
    req.params.nickname = None

    database.connect()
    try:
        if request_is_numeric():
            req.params.person = int(req.info.options[0])
            req.params.nickname = database.person.select_nickname(
                req.params.person)
        else:
            req.params.nickname = req.info.options[0]
            req.params.person = database.person.select_serial(
                req.params.nickname)
        if req.params.person:
            req.params.show_factories = database.factory.select_by_owner(
                req.params.person)
    finally:
        database.disconnect()


def redirect():
    """
    Redirect if the website address can be shown in the URL.
    """
    if request_is_numeric():
        location = '%s://%s/person/%s' % (
            req.info.uri.protocol, req.info.uri.hostname, req.params.nickname)
        util.redirect(req, location)


def title():
    """
    Page title.
    """
    return "Screenshot factories run by %s" % req.params.nickname


def body():
    """
    Write XHTML body content.
    """
    if req.params.show_factories:
        factory_list.write()
