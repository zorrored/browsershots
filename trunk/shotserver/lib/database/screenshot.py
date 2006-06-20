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

def select_by_hashkey(hashkey):
    """
    Get info about a screenshot.
    """
    cur.execute("""\
SELECT screenshot, screenshot.factory, screenshot.browser,
       screenshot.width, screenshot.height, screenshot.created,
       website, url
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN website USING (website)
WHERE hashkey = %s
""", (hashkey, ))
    return cur.fetchone()

def select_by_serial(serial):
    """
    Get info about a screenshot.
    """
    cur.execute("""\
SELECT hashkey, factory, screenshot.browser, screenshot.width, screenshot.height, screenshot.created, website, url
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN website USING (website)
WHERE screenshot = %s
""", (serial, ))
    return cur.fetchone()

def select_recent(limit=50):
    """
    Get serials of the most recently uploaded screenshots, one per website.
    """
    cur.execute("""\
SELECT hashkey, screenshot.width, screenshot.height, url
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN website USING (website)
WHERE screenshot IN (
    SELECT MAX(screenshot) AS maximum
    FROM screenshot
    JOIN request USING (screenshot)
    JOIN request_group USING (request_group)
    JOIN website USING (website)
    GROUP BY website
    ORDER BY maximum DESC
    LIMIT %s)
ORDER BY screenshot DESC
""", (limit, ))
    return cur.fetchall()

def select_prevnext(direction, website, screenshot):
    """
    Get the most recently uploaded screenshots.
    """
    if direction == 'prev':
        where = "WHERE website = %s AND screenshot < %s ORDER BY screenshot DESC"
    elif direction == 'next':
        where = "WHERE website = %s AND screenshot > %s ORDER BY screenshot ASC"
    else:
        return None
    cur.execute("""\
SELECT hashkey, screenshot.width, screenshot.height
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
""" + where, (website, screenshot))
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
JOIN factory ON factory.factory = screenshot.factory
JOIN opsys ON opsys.opsys = factory.opsys
JOIN opsys_group ON opsys_group.opsys_group = opsys.opsys_group
WHERE website = %s
ORDER BY screenshot DESC
LIMIT %s
""", (website, limit))
    return cur.fetchall()

def count_uploads_by_factory(factory, timespan='1:00'):
    """
    How many uploads per hour?
    """
    cur.execute("""\
SELECT COUNT(*) FROM screenshot
WHERE factory = %s
AND created > NOW()-%s::interval
""", (factory, timespan))
    return cur.fetchone()[0]
