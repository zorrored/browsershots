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
Database interface for website table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def select_url(serial):
    """
    Get the URL from the database.
    """
    cur.execute("SELECT url FROM website WHERE website=%s", (serial, ))
    result = cur.fetchone()
    if result is None:
        return None
    return result[0]


def select_serial(url, insert = False):
    """
    Get the serial number from the database.
    If the URL is not found and the insert parameter is set to True,
    insert it into database and try again.
    """
    cur.execute("SELECT website FROM website WHERE url=%s", (url, ))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    if not insert:
        return None
    cur.execute("INSERT INTO website (url) VALUES (%s)", (url, ))
    cur.execute("SELECT lastval()")
    row = cur.fetchone()
    return row[0]
