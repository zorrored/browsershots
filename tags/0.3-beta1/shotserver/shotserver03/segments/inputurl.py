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
URL input for submitting a new URL.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import cgi
from shotserver03.interface import xhtml


def write(url):
    """
    Write XHTML form for submitting a new URL.
    """
    xhtml.write_open_tag_line('form', action="/website/", method="post")
    xhtml.write_open_tag_line('div', _class="blue background", _id="inputurl")

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Paste your web address here, starting with http://")
    xhtml.write_tag_line('br')
    quoted_url = cgi.escape(url, quote = True)
    xhtml.write_tag('input', _type="text", _id="url", _name="url",
                    value=quoted_url, _class="text")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    req.write('<br />\n')
    xhtml.write_tag_line('input', value="Start", _class="button",
                         _type="submit", _id="submit", _name="submit")
    xhtml.write_close_tag_line('div')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="inputurl"
    xhtml.write_close_tag_line('form')
