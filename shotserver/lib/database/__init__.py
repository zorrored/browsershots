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
A higher-level interface to the PostgreSQL database.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from pyPgSQL import PgSQL

def connect():
    """
    Connect to the browsershots database.
    """
    __builtins__['con'] = PgSQL.connect(database = 'shotserver03')
    __builtins__['cur'] = con.cursor()

def disconnect():
    """
    Disconnect from the browsershots database.
    """
    cur.close()
    con.commit()
    con.close()
    del __builtins__['cur']
    del __builtins__['con']
