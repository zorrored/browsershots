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
Home page.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml
from shotserver03.segments import inputurl, about, news, sponsors


class UnexpectedFieldName(Exception):
    """The posted input contained an unexpected field name."""
    pass


def title():
    """Page title."""
    return "Test your web design in different browsers"


def read_form():
    """
    Read the posted input.
    """
    result = {}
    accept_fields = 'error url'.split()
    for name in accept_fields:
        result[name] = ''
    for field in req.info.form.list:
        if field.name not in accept_fields:
            raise UnexpectedFieldName(field.name)
        value = field.value
        value = value.replace('<', '&lt;')
        value = value.replace('>', '&gt;')
        result[field.name] = value
    return result


def body():
    """
    Write the front page.
    """
    url = ''
    if req.info.form:
        parameters = read_form()
        if (parameters['error']):
            xhtml.write_tag('p', parameters['error'], _class="error")
        if (parameters['url']):
            url = parameters['url']
    inputurl.write(url)

    about.write()
    news.write()
    sponsors.write()
