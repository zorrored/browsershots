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
List queued screenshot requests.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
import cgi
from shotserver03.interface import xhtml, human
from shotserver03 import database


def title():
    """Return page title."""
    return "Screenshot Request Queue"


def body():
    """
    Write HTML page content.
    """
    database.connect()
    try:
        rows = database.request.websites_in_queue()
    finally:
        database.disconnect()

    now = time.time()
    xhtml.write_open_tag_line('table')
    xhtml.write_table_row(("Queued", "URL"), element="th")
    for row in rows:
        website, url, submitted = row
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', human.timespan(now - submitted))
        url = cgi.escape(url)
        link = xhtml.tag('a', url, href="/website/%s/" % website)
        xhtml.write_tag('td', link)
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
