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
A higher-level interface to the PostgreSQL database.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import pgdb

from shotserver03.database import browser, factory, factory_browser
from shotserver03.database import nonce, opsys, request, screenshot
from shotserver03.database import website, priority_domain, person


def connect(db_name = 'shotserver03'):
    """
    Connect to the browsershots database.
    """
    assert 'con' not in __builtins__
    __builtins__['con'] = pgdb.connect(database=db_name)
    assert 'cur' not in __builtins__
    __builtins__['cur'] = con.cursor()
    cur.lastval = lastval


def disconnect():
    """
    Disconnect from the browsershots database.
    """
    if 'cur' in __builtins__:
        cur.close()
        del __builtins__['cur']
    if 'con' in __builtins__:
        con.commit()
        con.close()
        del __builtins__['con']


def insert(table, data):
    """
    Insert some values into a database table.
    data: A dictionary that contains the given keys.

    >>> insert('test', {'name': 'abc', 'value': 123, 'empty': None})
    INSERT INTO test (empty, name, value) VALUES (NULL, 'abc', 123)
    """
    keys = data.keys()
    keys.sort()
    columns = ', '.join(keys)
    references = '%(' + ')s, %('.join(keys) + ')s'
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, references)
    cur.execute(sql, data)


def lastval():
    """
    Return the value of the last sequence that was increased.
    Available since PostgreSQL version 8.1.
    Similar to MySQL's insert_id().
    """
    cur.execute("SELECT lastval()")
    return cur.fetchone()[0]


class Printer:
    """Emulate a cursor for use with doctest."""
    @staticmethod

    def execute(sql, data):
        """
        Print SQL data with a little bit of quoting.
        Parameter semantics similar to cursor.execute().

        >>> Printer.execute(INSERT INTO test (a, b) VALUES (%(a)s, %(b)s)',
                            {'a': 'ab\\'c%', 'b': 4, 'c': None})
        INSERT INTO test (a, b) VALUES ('ab\\'c%', 4)

        >>> Printer.execute('SELECT * FROM test a LIKE %s AND c IS %s',
                            ('ab\\'c%', None))
        SELECT * FROM test WHERE a LIKE 'ab\\'c%' AND c IS NULL
        """
        if type(data) == dict:
            copy = data.copy()
            keys = copy.keys()
        if type(data) == tuple:
            data = list(data)
        if type(data) == list:
            copy = data[:]
            keys = range(len(copy))
        for key in keys:
            value = copy[key]
            if type(value) == str:
                value = value.replace("'", "\\'")
                value = value.replace('"', '\\"')
                value = "'%s'" % value
            elif value is None:
                value = 'NULL'
            copy[key] = value
        if type(copy) == list:
            copy = tuple(copy)
        print sql % copy

if __name__ == '__main__':
    import sys
    import doctest
    cur = Printer()
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
