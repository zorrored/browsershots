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
Display bottom line with some links.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write_menu(_class, items):
    """
    Write XHTML <ul> with menu entries.
    """
    xhtml.write_open_tag('ul', _class=_class)
    for index, item in enumerate(items):
        text, link = item.split('=', 1)
        if index == 0:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link, _class="first"))
        else:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link))
    xhtml.write_close_tag_line('ul') # class="float-right"


def write():
    """
    Write bottom menu.
    """
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_open_tag_line('div', _class="menu lightgray", _id="bottom")

    write_menu('float-left', (
        "Contact=http://trac.browsershots.org/wiki/ContactDetails",
        "Terms of Use=http://trac.browsershots.org/wiki/TermsOfUse",
        "Privacy Policy=http://trac.browsershots.org/wiki/PrivacyPolicy"))

    write_menu('float-right', (
        "XHTML 1.1=http://validator.w3.org/check?uri=referer",
        "CSS=http://jigsaw.w3.org/css-validator/check/referer"))

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="bottom"
