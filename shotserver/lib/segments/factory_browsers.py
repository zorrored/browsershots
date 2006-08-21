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
Display browsers that are supported by a factory.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database

def write():
    """
    Write XHTML table with browsers supported by req.params.factory.
    """
    xhtml.write_tag_line('p',
        "This page shows the configuration of the screenshot factory %s."
        % xhtml.tag('b', req.params.factory_name))
    database.connect()
    try:
        rows = database.factory.browsers(req.params.factory)
        xhtml.write_open_tag_line('table', _id="factory-browser")
        xhtml.write_table_row((
            "Browser",
            "Engine",
            "Manufacturer",
            # "Last poll",
            # "Last upload",
            # "Uploads per hour",
            # "Uploads per day",
            ), element="th")
        for row in rows:
            (name, major, minor, engine, manufacturer) = row
            xhtml.write_open_tag('tr')
            # link = xhtml.tag('a', name, href="/browsers/" + name)
            browser = database.browser.version_string(name, major, minor)
            xhtml.write_tag('td', browser)
            xhtml.write_tag('td', engine)
            xhtml.write_tag('td', manufacturer)
            # per_hour = database.screenshot.count_uploads_by_factory(factory)
            # xhtml.write_tag('td', per_hour)
            xhtml.write_close_tag_line('tr')
        xhtml.write_close_tag_line('table')
    finally:
        database.disconnect()
