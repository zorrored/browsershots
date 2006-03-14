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

thumbdir = 'png/60'
max_thumbs = 30

def write():
    xhtml.write_open_tag_line('div', _id="recent")
    
    images = os.listdir('/var/www/browsershots.org/' + thumbdir)
    images.sort()
    for index, image in enumerate(images):
        if index == max_thumbs:
            break
        xhtml.write_tag_line('img', src='/'.join(('', thumbdir, image)), alt="", _class="absolute", style="right:%dpx" % (4 + index * 64))

    xhtml.write_close_tag_line('div') # id="recent"
