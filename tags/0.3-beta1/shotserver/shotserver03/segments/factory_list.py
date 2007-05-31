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
Display factories overview.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database


def write():
    """
    Write XHTML table with factories overview.
    """
    now = time.time()
    xhtml.write_open_tag_line('table', _id="factories")
    xhtml.write_table_row((
        "Factory<br />name",
        "Admin",
        "Operating<br />system",
        "Last<br />poll",
        "Last<br />upload",
        "Uploads<br />per hour",
        "Uploads<br />per day",
        ), element="th")
    for index, row in enumerate(req.params.show_factories):
        (factory, name, owner,
         opsys, distro, major, minor, codename,
         last_poll, last_upload, per_hour, per_day) = row
        xhtml.write_open_tag('tr', _class="color%d" % (index % 2 + 1))
        link = xhtml.tag('a', name, href="/factories/" + name)
        xhtml.write_tag('td', link)
        xhtml.write_tag('td', owner)
        opsys = database.opsys.version_string(
            opsys, distro, major, minor, codename)
        xhtml.write_tag('td', opsys)

        if last_poll is not None:
            last_poll = human.timespan(now - last_poll)
        xhtml.write_tag('td', last_poll)

        if last_upload is not None:
            last_upload = human.timespan(now - last_upload)
        xhtml.write_tag('td', last_upload)

        if per_hour == 0:
            per_hour = None
        xhtml.write_tag('td', per_hour)

        if per_day == 0:
            per_day = None
        xhtml.write_tag('td', per_day)

        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
