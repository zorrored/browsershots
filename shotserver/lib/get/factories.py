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
        cur.execute("""SELECT factory.name, os.name, distro, major, minor, codename
            FROM factory
            JOIN os_version USING (os_version)
            JOIN os USING (os)
            ORDER BY os.name, major, minor, factory.name
            """)
        result = cur.fetchall()
    finally:
        database.disconnect()

    xhtml.write_open_tag_line('table')
    for name, os, distro, major, minor, codename in result:
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', name)
        if distro is not None:
            os = '%s %s' % (os, distro)
        if major is not None:
            if minor is not None:
                os = '%s %d.%d' % (os, major, minor)
            else:
                os = '%s %d' % (os, major)
        if codename is not None:
            os = '%s (%s)' % (os, codename)
        xhtml.write_tag('td', os)
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
