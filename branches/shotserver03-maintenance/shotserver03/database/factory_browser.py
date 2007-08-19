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
Database interface for factory_browser table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def get_command(factory, browser, major, minor):
    """Get a different command from the database, if applicable."""
    cur.execute("""\
SELECT command
FROM factory_browser
JOIN browser_group USING (browser_group)
WHERE factory = %s
AND browser_group.name = %s
AND major = %s AND minor = %s
    """, (factory, browser, major, minor))
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    if result is None:
        result = browser.lower()
    return result


def factory_browsers(factory):
    """Get the browsers that are supported by this factory."""
    cur.execute("""\
SELECT factory_browser, browser_group.name, version,
engine.name, engine_version,
manufacturer, command,
extract(epoch from last_upload)::bigint AS last_upload,
extract(epoch from disabled)::bigint AS disabled
FROM factory_browser
JOIN browser_group USING (browser_group)
LEFT JOIN engine USING (engine)
WHERE factory = %s
ORDER BY browser_group.name, major, minor
""", (factory, ))
    return cur.fetchall()


def update_last_upload(factory_browser):
    """Set the last upload timestamp to NOW()."""
    cur.execute("""\
UPDATE factory_browser
SET last_upload = NOW()
WHERE factory_browser = %s
""", (factory_browser, ))


def active_browsers(where):
    """
    Get browsers on active factories.
    """
    cur.execute("""\
SELECT DISTINCT browser_group.name,
factory_browser.major, factory_browser.minor
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser_group USING (browser_group)
WHERE %s
AND factory.last_poll > NOW()-'0:10'::interval
AND factory_browser.disabled IS NULL
ORDER BY browser_group.name, factory_browser.major, factory_browser.minor
""" % where)
    return cur.fetchall()
