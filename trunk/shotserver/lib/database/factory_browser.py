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
Database interface for factory_browser table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def get_command(factory, browser, major, minor):
    """Get a different command from the database, if applicable."""
    cur.execute("""\
SELECT command
FROM factory_browser
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE factory = %s
AND browser_group.name = %s
AND major = %s AND minor = %s
    """, (factory, browser, major, minor))
    result = cur.fetchone()
    if result is None:
        return None
    return result[0]

def browsers(factory):
    """Get the browsers that are supported by this factory."""
    cur.execute("""\
SELECT browser, browser_group.name, major, minor, engine.name, manufacturer, command
FROM factory_browser
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
LEFT JOIN engine USING (engine)
WHERE factory = %s
ORDER BY browser_group.name, major, minor
""", (factory, ))
    return cur.fetchall()
