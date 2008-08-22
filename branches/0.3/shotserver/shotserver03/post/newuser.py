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
Insert a new user into the database.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import urllib
import re
from mod_python import util
from shotserver03 import database

email_match = re.compile(r'^.+@[^\.].*\.[a-z]{2,}$').match


class UnexpectedInput(Exception):
    """Post form input had unexpected fields."""
    pass


def read_form(form):
    """
    Get known fields from post form.
    Raise UnexpectedInput if field name is not known.
    """
    fields = {}
    known_keys = 'fullname email username password repeat'.split()
    for key in known_keys:
        fields[key] = ''
    for key in form.keys():
        if key in known_keys:
            fields[key] = form[key]
        elif key == 'submit':
            pass
        else:
            raise UnexpectedInput(key)
    return fields


def error_redirect(**params):
    """
    Redirect back to input form because an error has occurred.
    """
    params = urllib.urlencode(params)
    if params:
        util.redirect(req, '/newuser?' + params)
    else:
        util.redirect(req, '/newuser')


def sanity_check(fields):
    """Check input values for obvious errors."""
    # Email address
    if not email_match(fields['email']):
        fields['email_error'] = "Email address looks invalid"
    # Repeat password
    if fields['password'] != fields['repeat']:
        fields['repeat_error'] = "Password and repeat are different"
    # Empty fields
    if fields['fullname'].strip() == '':
        fields['fullname_error'] = "Full name not specified"
    if fields['email'].strip() == '':
        fields['email_error'] = "Email not specified"
    if fields['username'].strip() == '':
        fields['username_error'] = "Username not specified"
    if fields['password'].strip() == '':
        fields['password_error'] = "Password not specified"
    if fields['repeat'].strip() == '':
        fields['repeat_error'] = "Repeat not specified"
    for key in fields:
        if key.endswith('_error'):
            del(fields['password'])
            del(fields['repeat'])
            error_redirect(**fields)


def redirect():
    """
    Insert new user into database.
    Redirect to overview page on success.
    Redirect back to input form on error.
    """
    fields = read_form(req.info.form)
    sanity_check(fields)

    database.connect()
    try:
        person = database.person.insert(fields)
    finally:
        database.disconnect()

    util.redirect(req, '/person/%d/' % person)
