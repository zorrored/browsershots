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
Display meta menu.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('div', _class="menu", _id="metamenu")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'Home', href="/"+req.info.uri.lang),  _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Blog', href="/blog/"))
    xhtml.write_tag('li', xhtml.tag('a', 'Roadmap', href="/trac/roadmap/"))
    xhtml.write_tag('li', xhtml.tag('a', 'History', href="/trac/timeline/"))
    xhtml.write_tag('li', xhtml.tag('a', 'Help', href="/trac/wiki/HelpIndex"))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_open_tag_line('form', action="")
    xhtml.write_open_tag_line('div', _class="right")
    # xhtml.write_tag_line('input', _type="text")
    # xhtml.write_tag_line('input', _type="submit", value="Search")
    
    xhtml.write_open_tag_line('select', _id="langsel",
        onchange="document.location.href=this.form.langsel.options[this.form.langsel.options.selectedIndex].value")
    xhtml.write_tag_line('option', 'Deutsch', value="de")
    xhtml.write_tag_line('option', 'English (American)', value="en-US")
    xhtml.write_tag_line('option', 'English (British)', value="en-GB")
    xhtml.write_tag_line('option', 'Português do Brazil', value="pt-BR")
    xhtml.write_tag_line('option', 'Български', value="bg")
    xhtml.write_tag_line('option', '正體中文', value="zh")
    xhtml.write_close_tag_line('select')
    xhtml.write_close_tag_line('div')
    xhtml.write_close_tag_line('form')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="metamenu"
