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
Database interface for screenshot table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def select_recent(limit=50):
    """
    Get the most recently uploaded screenshots.
    """
    cur.execute("""\
SELECT hashkey, screenshot.width, screenshot.height, url
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN website USING (website)
ORDER BY screenshot.created DESC
LIMIT %s
""", (limit, ))
    return cur.fetchall()

def select_recent_website(website, limit=5):
    """
    Get the most recently uploaded screenshots for a website.
    """
    cur.execute("""\
SELECT hashkey,
       browser_group.name, browser.major, browser.minor,
       opsys_group.name,
       extract(epoch from screenshot.created)::bigint
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN browser ON browser.browser = screenshot.browser
JOIN browser_group ON browser_group.browser_group = browser.browser_group
JOIN factory USING (factory)
JOIN opsys ON opsys.opsys = factory.opsys
JOIN opsys_group ON opsys_group.opsys_group = opsys.opsys_group
WHERE website = %s
ORDER BY screenshot.created DESC
LIMIT %s
""", (website, limit))
    return cur.fetchall()
