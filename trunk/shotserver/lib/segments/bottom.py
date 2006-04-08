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

def write():
    xhtml.write_open_tag_line('div', _class="menu lightgray", _id="bottom")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'FAQ', href="/trac/wiki/FrequentlyAskedQuestions"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Terms of Use', href="/trac/wiki/TermsOfUse"))
    xhtml.write_tag('li', xhtml.tag('a', 'Privacy Policy', href="/trac/wiki/PrivacyPolicy"))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_open_tag('ul', _class="right")
    xhtml.write_tag('li', xhtml.tag('a', 'XHTML 1.1', href="http://validator.w3.org/check?uri=referer"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'CSS', href="http://jigsaw.w3.org/css-validator/check/referer"))
    xhtml.write_close_tag_line('ul') # class="right"

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="bottom"
