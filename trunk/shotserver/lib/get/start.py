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
Home page.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml
from shotserver03.segments import inputurl, about, news, sponsors

def title():
    return "Test your web design in different browsers"

class UnexpectedFieldName(Exception):
    pass

def read_form():
    result = {}
    accept_fields = 'error url'.split()
    for name in accept_fields:
        result[name] = ''
    for field in req.info.form.list:
        if field.name not in accept_fields:
            raise UnexpectedFieldName(field.name)
        result[field.name] = field.value
    return result

def body():
    # xhtml.write_tag_line('p', "<b>Status:</b> A design study, a technology preview, a work in progress.")
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
