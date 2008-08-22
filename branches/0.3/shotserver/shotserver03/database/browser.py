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
Database interface for browser table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def get_name_dict():
    """
    Get a mapping from lowercase browser name to id (numeric primary key).
    """
    cur.execute("SELECT browser_group, name FROM browser_group")
    result = {}
    for browser, name in cur.fetchall():
        result[name.lower()] = browser
    return result


def select_by_user_agent(factory, user_agent):
    """
    Select the browser with a given User-Agent string.
    """
    cur.execute("""\
SELECT factory_browser, browser_group.name, major, minor
FROM factory_browser
JOIN browser_group USING (browser_group)
WHERE factory = %s
AND user_agent = %s
""", (factory, user_agent, ))
    return cur.fetchone()


def version_string(browser, major=None, minor=None):
    """
    Make a string with browser name and version number.
    The version number parts will be skipped if None.
    """
    result = [browser]
    if major is not None:
        result.append(' %d' % major)
        if minor is not None:
            result.append('.%d' % minor)
    return ''.join(result)
