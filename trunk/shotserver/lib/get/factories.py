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
List all factories.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml
from shotserver03 import database

def title():
    """Return page title."""
    return "Screenshot Factories"

def body():
    """
    Write HTML page content.
    """
    database.connect()
    try:
        cur.execute("""SELECT factory.name, opsys.name, distro, major, minor, codename
            FROM factory
            JOIN opsys_version USING (opsys_version)
            JOIN opsys USING (opsys)
            ORDER BY opsys.name, major, minor, factory.name
            """)
        result = cur.fetchall()
    finally:
        database.disconnect()

    xhtml.write_open_tag_line('table')
    for name, opsys, distro, major, minor, codename in result:
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', name)
        if distro is not None:
            opsys = '%s %s' % (opsys, distro)
        if major is not None:
            if minor is not None:
                opsys = '%s %d.%d' % (opsys, major, minor)
            else:
                opsys = '%s %d' % (opsys, major)
        if codename is not None:
            opsys = '%s (%s)' % (opsys, codename)
        xhtml.write_tag('td', opsys)
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
