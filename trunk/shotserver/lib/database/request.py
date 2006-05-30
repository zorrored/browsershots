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
Database interface for website table.
"""

__revision__ = '$Rev: 117 $'
__date__ = '$Date: 2006-04-08 08:51:18 +0200 (Sat, 08 Apr 2006) $'
__author__ = '$Author: johann $'

def select_by_website(website):
    """
    Get all jobs for this website.
    """
    sql = []
    sql.append("SELECT browser.name, major, minor, os.name, width, bpp, javascript, java, flash, media")
    sql.append(", extract(epoch from request.created)::bigint, expire")
    sql.append("FROM request")
    sql.append("JOIN browser USING (browser)")
    sql.append("JOIN os USING (os)")
    sql.append("WHERE website=%s")
    sql.append("ORDER BY browser.name, major, minor, os.name")
    # sql.append("JOIN media ON media")
    sql = ' '.join(sql)
    cur.execute(sql, (website, ))
    return cur.fetchall()
