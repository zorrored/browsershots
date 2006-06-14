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
Database interface for lock table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import pgdb

def attempt(factory, request):
    """
    Lock a screenshot request to make sure that no other factory is
    working on it.
    """
    con.commit()
    try:
        cur.execute("INSERT INTO lock VALUES (%s, %s)", (request, factory))
        return True
    except pgdb.DatabaseError: # Try to remove an expired lock.
        con.rollback()
        cur.execute("SELECT factory FROM lock WHERE request = %s", (request, ))
        row = cur.fetchone()
        if row is not None:
            cur.execute("INSERT INTO failure (request, factory) VALUES (%s, %s)",
                        (request, row[0]))
            cur.execute("DELETE FROM lock WHERE request = %s", (request, ))
            cur.execute("INSERT INTO lock VALUES (%s, %s)", (request, factory))
