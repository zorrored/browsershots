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
URL input for submitting new jobs.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('form', action="/website/", method="post")
    xhtml.write_open_tag_line('div', _id="inputurl")
    xhtml.write_tag_line('p', "Paste your web address here, starting with http://")
    xhtml.write_tag_line('input', _type="text", _id="url", _name="url", value="", _class="text")
    xhtml.write_tag_line('input', _type="submit", _id="submit", _name="submit", value="Start", _class="button")
    xhtml.write_close_tag_line('div')
    xhtml.write_close_tag_line('form')
