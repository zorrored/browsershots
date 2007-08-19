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
Display browsers that are installed on a factory.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database


def write():
    """
    Write XHTML table with browsers installed on req.params.factory.
    """
    factory = req.params.factory
    now = time.time()
    database.connect()
    try:
        rows = database.factory_browser.factory_browsers(factory)
        xhtml.write_open_tag_line('table', _id="factory-browser")
        xhtml.write_table_row((
            "Browser",
            "Engine",
            "Maker",
            "Last<br />upload",
            "Uploads<br />per hour",
            "Uploads<br />per day",
            "",
            ), element="th")
        for index, row in enumerate(rows):
            (factory_browser, name, version, engine, engine_version,
             manufacturer, command, last_upload, disabled) = row
            if disabled:
                xhtml.write_open_tag('tr',
                                     _class="color%d gray" % (index % 2 + 1))
            else:
                xhtml.write_open_tag('tr', _class="color%d" % (index % 2 + 1))
            # link = xhtml.tag('a', name, href="/browsers/" + name)
            xhtml.write_tag('td', name + ' ' + version)
            if engine_version:
                xhtml.write_tag('td', engine + ' ' + engine_version)
            else:
                xhtml.write_tag('td', engine)
            xhtml.write_tag('td', manufacturer)

            if last_upload is not None:
                last_upload = human.timespan(now - last_upload)
            xhtml.write_tag('td', last_upload)

            per_hour = database.screenshot.count_uploads(
                'factory_browser=%s', (factory_browser, ), '1:00')
            if per_hour == 0:
                per_hour = None
            xhtml.write_tag('td', per_hour)

            per_day = database.screenshot.count_uploads(
                'factory_browser=%s', (factory_browser, ), '24:00')
            if per_day == 0:
                per_day = None
            xhtml.write_tag('td', per_day)

            if disabled:
                xhtml.write_tag('td', '(disabled)')
            elif command:
                xhtml.write_tag('td', command)
            else:
                xhtml.write_tag('td', '')

            xhtml.write_close_tag_line('tr')
        xhtml.write_close_tag_line('table')
    finally:
        database.disconnect()
