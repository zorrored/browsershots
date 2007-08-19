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
Display previous and next screenshot.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from math import sqrt
from shotserver03 import database
from shotserver03.interface import xhtml


def write(direction='prev'):
    """
    Write XHTML div with previous and next screenshot.
    """
    database.connect()
    try:
        rows = database.screenshot.select_prevnext(
            direction, req.params.website, req.params.screenshot)
    finally:
        database.disconnect()

    if direction == 'prev':
        last = "You are at the oldest screenshot."
        inside = 'right'
        outside = 'left'
    else:
        last = "You are at the newest screenshot."
        inside = 'left'
        outside = 'right'
    xhtml.write_open_tag_line('div', _id=direction, _class=outside)
    if len(rows) == 0:
        xhtml.write_tag_line('p', last, _class="up "+inside)
    else:
        link = '/screenshots/%s/' % rows[0][0]
        if direction == 'prev':
            link = xhtml.tag('a', "Older", href=link)
            xhtml.write_tag_line('p', link, _class="up bold right")
        else:
            link = xhtml.tag('a', "Newer", href=link)
            xhtml.write_tag_line('p', link, _class="up bold left")
        for index, row in enumerate(rows):
            if index == 3:
                xhtml.write_tag_line('p', '%d more...' %
                                     (len(rows) - 3), _class="up")
                break
            hashkey, width, height = row
            zoom = int(1000 / sqrt(index + 1))
            height = height * 140 / width * zoom / 1000
            width = 140 * zoom / 1000
            prefix = hashkey[:2]
            img = xhtml.tag('img',
                            src='/png/140/%s/%s.png' % (prefix, hashkey),
                            width=width, height=height, alt="")
            xhtml.write_tag('a', img, href='/screenshots/%s/' % hashkey)
            xhtml.write_tag_line('br')
    xhtml.write_close_tag_line('div') # id=direction
