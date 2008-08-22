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
Database interface for screenshot table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def hashkey_to_serial(hashkey):
    """
    Get the serial number of a screenshot.
    """
    cur.execute("""\
SELECT screenshot
FROM screenshot
WHERE hashkey = %s
""", (hashkey, ))
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result


def insert(hashkey, factory, factory_browser, width, height):
    """
    Insert a screenshot into the database.
    """
    cur.execute("""\
INSERT INTO screenshot
(hashkey, factory, factory_browser, width, height)
VALUES (%s, %s, %s, %s, %s)
""", (hashkey, factory, factory_browser, width, height))


def info(screenshot):
    """
    Get some info about this screenshot.
    """
    cur.execute("""\
SELECT extract(epoch from screenshot.created)::bigint AS uploaded,
screenshot.width, screenshot.height,
browser_group.name, factory_browser.version,
factory.name, opsys_group.name, distro, codename,
website, url
FROM screenshot
JOIN factory USING (factory)
JOIN factory_browser USING (factory_browser)
JOIN browser_group USING (browser_group)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
JOIN website USING (website)
WHERE screenshot = %s
""", (screenshot, ))
    return cur.fetchone()


def select_recent_websites(limit=50):
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
    WHERE screenshot.created>NOW()-'24:00'::interval
    GROUP BY website
    ORDER BY maximum DESC
    LIMIT %s)
ORDER BY screenshot DESC
""", (limit, ))
    return cur.fetchall()


def select_prevnext(direction, website, screenshot):
    """
    Get other screenshots before or after a given screenshot.
    """
    if direction == 'prev':
        where = """\
WHERE website = %s AND screenshot < %s
ORDER BY screenshot DESC"""
    elif direction == 'next':
        where = """\
WHERE website = %s AND screenshot > %s
ORDER BY screenshot ASC"""
    else:
        return None
    cur.execute("""\
SELECT hashkey, screenshot.width, screenshot.height
FROM screenshot
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
""" + where, (website, screenshot))
    return cur.fetchall()


def select_recent(where, args, limit=5):
    """
    Get the most recently uploaded screenshots for a website.
    """
    cur.execute("""\
SELECT hashkey, browser_group.name, factory_browser.version,
opsys_group.name, extract(epoch from screenshot.created)::bigint
FROM screenshot
JOIN factory USING (factory)
JOIN factory_browser USING (factory_browser)
JOIN browser_group USING (browser_group)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN request USING (screenshot)
JOIN request_group USING (request_group)
WHERE """ + where + """
ORDER BY screenshot DESC
LIMIT """ + str(limit), args)
    return cur.fetchall()


def count_uploads(where, args, timespan='1:00'):
    """
    How many uploads per hour for a factory?
    How many uploads per day for a browser on a factory?
    """
    args = list(args)
    args.append(timespan)
    cur.execute("""\
SELECT COUNT(*)
FROM screenshot
WHERE """ + where + """
AND created > NOW()-%s::interval
""", args)
    return cur.fetchone()[0]


def last_upload(where, args):
    """
    When was the last upload for a browser on a factory?
    """
    cur.execute("""\
SELECT extract(epoch from created)::bigint AS uploaded
FROM screenshot
WHERE """ + where + """
ORDER BY created DESC
LIMIT 1
""", args)
    result = cur.fetchone()
    if result is not None:
        result = result[0]
    return result
