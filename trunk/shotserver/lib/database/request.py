# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Database interface for request table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.database import options

def select_websites():
    """
    Get all queuing websites.
    """
    cur.execute("""\
SELECT website, url, extract(epoch from MAX(request_group.created))::bigint AS created
FROM request_group
JOIN website USING (website)
WHERE expire > NOW()
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

def select_match(where):
    """
    Get the oldest matching request from the queue.
    """
    cur.execute("""\
SELECT request,
       browser_group.name, major, minor,
       width, bpp, js, java, flash, media
FROM request
JOIN request_group USING (request_group)
JOIN website USING (website)
JOIN browser_group USING (browser_group)
LEFT JOIN opsys_group USING (opsys_group)
WHERE """ + where + """
AND request_group.expire >= NOW()
AND screenshot IS NULL
AND (NOT EXISTS (SELECT request FROM lock
                WHERE lock.request = request.request
                AND NOW() - lock.created <= %s))
AND (NOT EXISTS (SELECT request FROM failure
                WHERE failure.request = request.request
                AND NOW() - failure.created <= %s))
ORDER BY request_group.created
LIMIT 1
""", (options.lock_timeout, options.failure_timeout))
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
INSERT INTO request_group (website, width, bpp, js, java, flash, media, expire)
VALUES (%(website)s, %(width)s, %(bpp)s, %(js)s, %(java)s, %(flash)s, %(media)s, NOW() + %(expire)s)
""", values)
    return cur.lastval()

def update_browser(request, browser):
    """Set the browser for a request."""
    cur.execute("UPDATE request SET browser = %s, redirected = NOW() WHERE request = %s", (browser, request))

def update_screenshot(request, screenshot):
    """Set the screenshot for a request."""
    cur.execute("UPDATE request SET screenshot = %s WHERE request = %s", (screenshot, request))
