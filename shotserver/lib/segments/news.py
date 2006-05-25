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
Show the latest news headlines from the blog.
"""

__revision__ = '$Rev: 77 $'
__date__ = '$Date: 2006-03-29 00:48:25 +0200 (Wed, 29 Mar 2006) $'
__author__ = '$Author: johann $'

import re
from shotserver03.interface import xhtml

def cutoff(text, maxlen):
    if len(text) <= maxlen:
        return text
    cut = text.rfind(' ', 0, maxlen)
    if cut == -1:
        cut = maxlen - 1
    return text[:cut] + ' ...'

items = re.compile('<item>\s*<title>(.+?)</title>\s*<link>(http.+?)</link>').findall
def write():
    xhtml.write_open_tag_line('div', _id="news")
    xhtml.write_tag_line('h2', "Latest News")

    xhtml.write_open_tag_line('ul')
    rss = file('/var/www/browsershots.org/blog/rss.xml').read()
    for item in items(rss):
        title, link = item
        title = cutoff(title, 36)
        link = xhtml.tag('a', title, href=link)
        xhtml.write_tag_line('li', link)
    xhtml.write_close_tag_line('ul')

    xhtml.write_close_tag_line('div') # id="news"
