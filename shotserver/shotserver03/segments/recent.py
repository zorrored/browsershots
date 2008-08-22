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
Display recent screenshots in a horizontal row.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import cgi
from shotserver03.interface import xhtml
from shotserver03 import database


offensive_keywords = """
www.farmse porn pron p0rn pr0n boys girls chicks babe cock
sex xxx nude nudist naked bitcafe stile omglol
""".lower().split()


def offensive(url):
    """
    Return True if url contains a potentially offensive keyword.
    """
    url_lower = url.lower()
    for term in offensive_keywords:
        if url_lower.count(term):
            return True


def write():
    """
    Write XHTML div with recent screenshots.
    """
    database.connect()
    try:
        rows = database.screenshot.select_recent_websites()
    finally:
        database.disconnect()

    columns = [0] * 5
    xhtml.write_open_tag_line('div', _id="recent", _class="relative")
    for row_index, row in enumerate(rows):
        hashkey, width, height, url = row
        if offensive(url):
            continue
        height = height * 140 / width
        width = 140
        if row_index > 5 and height > (len(rows) - row_index) * 28:
            continue
        minimum = min(columns)
        smallest = columns.index(minimum)
        left = 156 * smallest
        top = columns[smallest]
        columns[smallest] += height + 16
        url = cgi.escape(url, quote=True)
        prefix = hashkey[:2]
        img = xhtml.tag('img', alt="Screenshot of %s" % url, title=url,
                        src='/png/140/%s/%s.png' % (prefix, hashkey),
                        width=width, height=height,
                        style="left:%dpx;top:%dpx;" % (left, top))
        xhtml.write_tag_line('a', img, href='/screenshots/%s/' % hashkey)
    xhtml.write_tag_line('div', '&nbsp;', style="height:%dpx;" % max(columns))
    xhtml.write_close_tag_line('div') # id="recent"
