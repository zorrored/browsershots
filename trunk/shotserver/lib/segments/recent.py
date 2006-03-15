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
Display recent screenshots in a horizontal row.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import os
from shotserver03.interface import xhtml

max_thumbs = 30

def write():
    xhtml.write_open_tag_line('div', _id="recent")

    lines = file('/var/www/browsershots.org/png/sizes.txt').readlines()
    for index, line in enumerate(lines):
        if index == max_thumbs:
            break
        image, width, height = line.split()
        width = int(width) / 4
        height = int(height) / 4
        img = xhtml.tag('img', src='/'.join(('', 'png', '120',image)), alt="", _class="absolute",
                        onmouseover="larger(this,%d,%d)" % (width, height),
                        onmouseout="smaller(this,%d,%d)" % (width, height),
                        style="right:%dpx;width:%dpx;height:%dpx;margin-right:-30px" % (32 + index * 64, width, height))
        xhtml.write_tag_line('a', img, href='png/240/%s' % image)

    xhtml.write_close_tag_line('div') # id="recent"
