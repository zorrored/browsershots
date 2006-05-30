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
Show all queued requests for a given website.
"""

__revision__ = '$Rev: 41 $'
__date__ = '$Date: 2006-03-15 07:46:49 +0100 (Wed, 15 Mar 2006) $'
__author__ = '$Author: johann $'

import time
from shotserver03.interface import xhtml
from shotserver03 import database

def write():
    database.connect()
    try:
        xhtml.write_open_tag('table', _id="queue")
        xhtml.write_table_row("Browser OS Width BPP JavaScript Java Flash Media Submitted Expires".split(), 'th')
        for browser, major, minor, os, width, bpp, javascript, java, flash, media, submitted, expire in database.request.select_by_website(req.params.website):
            if major is not None:
                browser += " %d" % major
            if minor is not None:
                browser += ".%d" % minor
            xhtml.write_table_row((browser, os, width, bpp, javascript, java, flash, media,
                                   time.strftime('%H:%M:%S', time.localtime(submitted)),
                                   time.strftime('%H:%M:%S', time.localtime(submitted + expire))))
        xhtml.write_close_tag_line('table') # id="queue"
    finally:
        database.disconnect()

