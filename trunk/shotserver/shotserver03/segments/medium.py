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
Show a medium-sized preview of a screenshot.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml


def write():
    """
    XHTML div with screenshot preview.
    """
    xhtml.write_open_tag_line('div', _id="medium")
    hashkey = req.params.hashkey
    height = (req.params.height*450 + req.params.width/2) / req.params.width
    prefix = hashkey[:2]
    img = xhtml.tag('img', src='/png/450/%s/%s.png' % (prefix, hashkey),
                    width=450, height=height, alt="")
    link = '/png/full/%s/%s.png' % (prefix, hashkey)
    xhtml.write_tag_line('a', img, href=link)
    xhtml.write_close_tag_line('div') # id="medium"
