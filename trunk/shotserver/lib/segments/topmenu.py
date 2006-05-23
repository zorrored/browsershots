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
Display top menu bar.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('div', _class="menu lightgray", _id="topmenu")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'Screenshots', href="/screenshots/"+req.info.uri.lang),  _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Queue', href="/queue/"+req.info.uri.lang))
    xhtml.write_tag('li', xhtml.tag('a', 'Factories', href="/factories/"+req.info.uri.lang))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_open_tag('ul', _class="right")
    xhtml.write_tag('li', xhtml.tag('a', 'Sign In', href="/signin/"), _class="first")
    xhtml.write_close_tag_line('ul') # class="right"

    link = xhtml.tag('a', 'Mock-up!', href="http://browsershots.org/blog/2006/03/15/mock-up-for-browsershots-0-3/")
    xhtml.write_tag_line('p', link, _class="right mockup")

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="topmenu"

