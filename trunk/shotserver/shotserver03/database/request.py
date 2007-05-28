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
Database interface for request table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.database import options


def websites_in_queue():
    """
    Get all queuing websites.
    """
    cur.execute("""\
SELECT website, url,
extract(epoch from MAX(request_group.created))::bigint AS created
FROM request_group
JOIN request USING (request_group)
JOIN website USING (website)
WHERE expire > NOW()
AND screenshot IS NULL
GROUP BY website, url
ORDER BY created
""")
    return cur.fetchall()


def select_by_website(website):
    """
    Get all request groups for this website.
    """
    cur.execute("""\
SELECT DISTINCT request_group,
       width, bpp, js, java, flash, media,
       extract(epoch from created)::bigint AS created,
       extract(epoch from expire)::bigint AS expire
FROM request_group
JOIN request USING (request_group)
WHERE website = %s
AND expire > NOW()
AND screenshot IS NULL
ORDER BY created
""", (website, ))
    return cur.fetchall()


def select_by_group(group):
    """
    Get all requests in a request group.
    """
    cur.execute("""\
SELECT DISTINCT browser_group.name, major, minor, opsys_group
FROM request
JOIN browser_group USING (browser_group)
LEFT JOIN opsys_group USING (opsys_group)
WHERE request_group = %s
AND screenshot IS NULL
ORDER BY browser_group.name, major, minor
""", (group, ))
    return cur.fetchall()


def select_match(where, order='ASC'):
    """
    Get the oldest matching request from the queue.
    """
    cur.execute("""\
SELECT request,
       browser_group.name, major, minor,
       width, bpp, js, java, flash, media
FROM request
JOIN request_group USING (request_group)
JOIN browser_group USING (browser_group)
LEFT JOIN opsys_group USING (opsys_group)
WHERE """ + where + """
AND screenshot IS NULL
AND (locked IS NULL OR NOW() - locked > %s)
ORDER BY priority desc, request_group.created """ + order + """
LIMIT 1
""", (options.lock_timeout, ))
    return cur.fetchone()


def to_dict(row):
    """
    Make an option dictionary from a result row from the match() function.
    """
    keys = 'request browser major minor width bpp js java flash media'.split()
    integer_keys = 'request major minor width bpp'.split()
    result = {}
    for index, key in enumerate(keys):
        value = row[index]
        if value is None:
            if key in integer_keys:
                value = 0
            else:
                value = ''
        result[key] = value
    return result


def insert_group(values):
    """
    Insert a request group into the database.
    """
    cur.execute("""\
INSERT INTO request_group
(website, width, bpp, js, java, flash, media, expire)
VALUES (%(website)s, %(width)s, %(bpp)s,
%(js)s, %(java)s, %(flash)s, %(media)s, NOW() + %(expire)s)
""", values)
    return cur.lastval()


def find_identical_groups(values):
    """
    Find request groups with the same options.
    """
    cur.execute("""\
SELECT request_group FROM request_group
WHERE website = %(website)s
AND (width IS NULL OR width = %(width)s)
AND (bpp IS NULL OR bpp = %(bpp)s)
AND (js IS NULL OR js = %(js)s)
AND (java IS NULL OR java = %(java)s)
AND (flash IS NULL OR flash = %(flash)s)
AND (media IS NULL OR media = %(media)s)
""", values)
    result = []
    for row in cur.fetchall():
        result.append(str(row[0]))
    return ','.join(result)


def delete_identical(values, groups):
    """
    Avoid duplication: when inserting new requests, first delete
    identical requests (unless they've been locked). This delete will
    also cascade to the failure table.
    """
    cur.execute("""\
DELETE FROM request
WHERE (browser_group IS NULL OR browser_group = %(browser_group)s)
AND (major IS NULL OR major = %(major)s)
AND (minor IS NULL OR minor = %(minor)s)
AND (opsys_group IS NULL OR opsys_group = %(opsys_group)s)
AND locked IS NULL
AND request_group IN (""" + groups + """)
""", values)


def insert(values):
    """
    Insert a new request into the database.
    """
    cur.execute("""\
INSERT INTO request
(request_group, browser_group, major, minor, opsys_group, priority)
VALUES (%(request_group)s, %(browser_group)s, %(major)s, %(minor)s,
        %(opsys_group)s, %(priority)s)
""", values)


def update_locked(request, factory):
    """Set the lock and factory."""
    cur.execute("""\
UPDATE request SET factory = %s, locked = NOW()
WHERE request = %s
""", (factory, request))


def update_browser(request, factory_browser):
    """Set the factory_browser for a request."""
    cur.execute("""\
UPDATE request
SET factory_browser = %s, redirected = NOW()
WHERE request = %s
""", (factory_browser, request))


def update_screenshot(request, screenshot):
    """Set the screenshot for a request."""
    cur.execute("""\
UPDATE request SET screenshot = %s
WHERE request = %s
""", (screenshot, request))
