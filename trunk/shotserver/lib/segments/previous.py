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
Display previous screenshots.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import random
from shotserver03 import database
from shotserver03.interface import xhtml

def write():
    """
    Write XHTML div with previous screenshots.
    """
    database.connect()
    try:
        rows = database.screenshot.select_previous(req.params.website, req.params.screenshot)
    finally:
        database.disconnect()

    xhtml.write_open_tag_line('div', _id="previous")
    xhtml.write_tag_line('h2', "Previous")
    for row in rows:
        hashkey, width, height = row
        height = height * 140 / width
        width = 140
        prefix = hashkey[:2]
        img = xhtml.tag('img', src='/png/140/%s/%s.png' % (prefix, hashkey),
                        width=width, height=height, alt="")
        xhtml.write_tag_line('a', img, href='/screenshots/%s/' % hashkey)
    xhtml.write_close_tag_line('div') # id="previous"
