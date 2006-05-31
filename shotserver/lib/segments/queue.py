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
    """
    Write XHTML table with queued requests for a given website.
    """
    database.connect()
    try:
        xhtml.write_open_tag('table', _id="queue")
        xhtml.write_table_row("Browser OS Width Submitted Expires Options".split(), 'th')
        for request in database.request.select_by_website(req.params.website):
            browser, major, minor, opsys, width, bpp, javascript, java, flash, media, submitted, expire = request
            if major is not None:
                browser += " %d" % major
            if minor is not None:
                browser += ".%d" % minor
            options = []
            if bpp is not None:
                options.append("%d BPP" % bpp)
            if javascript is not None:
                options.append("JavaScript")
            if java is not None:
                options.append("Java")
            if flash is not None:
                options.append("Flash")
            if media is not None:
                if media == 'wmp':
                    options.append(media)
                else:
                    options.append("Windows Media Player")
            xhtml.write_table_row((browser, opsys, width,
                                   time.strftime('%H:%M', time.localtime(submitted)),
                                   time.strftime('%H:%M', time.localtime(submitted + expire)),
                                   ', '.join(options)))
        xhtml.write_close_tag_line('table') # id="queue"
    finally:
        database.disconnect()
