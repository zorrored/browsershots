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
Check formatting of Python source code.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write_top():
    xhtml.write_open_tag_line('div', _class="menu", _id="top")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'Home', href="/"),  _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Trac', href="/trac/"))
    xhtml.write_tag('li', xhtml.tag('a', 'Blog', href="/blog/"))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_open_tag('ul', _class="right")
    xhtml.write_tag('li', xhtml.tag('a', 'Settings', href="/settings/"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Sign Out', href="/signout/"))
    xhtml.write_close_tag_line('ul') # class="right"

    xhtml.write_tag_line('p', '60 seconds', _class="right")
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="top"

def write_sub():
    xhtml.write_open_tag_line('div', _class="menu", _id="sub")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'Screenshots', href="/screenshots/"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Submit', href="/submit/"))
    xhtml.write_tag('li', xhtml.tag('a', 'Search', href="/search/"))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="sub"

def write_sponsors():
    xhtml.write_open_tag('p', _id="sponsors")
    req.write("Sponsored by ")
    xhtml.write_tag('img', src="style/mfg.png", alt="MFG Stiftung BW")
    xhtml.write_close_tag_line('p') # id="sponsors"

def write_bottom():
    xhtml.write_open_tag_line('div', _class="menu", _id="bottom")

    xhtml.write_open_tag('ul', _class="left")
    xhtml.write_tag('li', xhtml.tag('a', 'FAQ', href="/trac/wiki/FrequentlyAskedQuestions/"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'Terms of Use', href="/trac/wike/TermsOfUse/"))
    xhtml.write_tag('li', xhtml.tag('a', 'Privacy Policy', href="/trac/wike/PrivacyPolicy/"))
    xhtml.write_close_tag_line('ul') # class="left"

    xhtml.write_open_tag('ul', _class="right")
    xhtml.write_tag('li', xhtml.tag('a', 'XHTML 1.1', href="http://validator.w3.org/check?uri=referer"), _class="first")
    xhtml.write_tag('li', xhtml.tag('a', 'CSS', href="http://jigsaw.w3.org/css-validator/check/referer"))
    xhtml.write_close_tag_line('ul') # class="right"

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="bottom"

