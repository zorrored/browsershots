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
Database interface for request table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def select_by_website(website):
    """
    Get all jobs for this website.
    """
    cur.execute("""\
SELECT request, bpp, js, java, flash, media
, extract(epoch from request.created)::bigint, expire
FROM request
WHERE website=%s
ORDER BY created
""", (website, ))
    return cur.fetchall()

def match(where):
    """
    Get the oldest matching request that isn't expired.
    """
    cur.execute("""\
SELECT url, browser.name, major, minor, width, bpp, js, java, flash, media
FROM request
JOIN request_browser USING (request)
JOIN website USING (website)
JOIN browser USING (browser)
WHERE request.expire >= NOW() AND %s
ORDER BY request.created
LIMIT 1
""" % where)
    return cur.fetchone()
