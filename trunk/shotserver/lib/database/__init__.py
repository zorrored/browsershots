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
A higher-level interface to the PostgreSQL database.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import pgdb
from shotserver03.database import browser, factory, lock, nonce, opsys, request, website

def connect():
    """
    Connect to the browsershots database.
    """
    __builtins__['con'] = pgdb.connect(database = 'shotserver03')
    __builtins__['cur'] = con.cursor()
    cur.lastval = lastval

def disconnect():
    """
    Disconnect from the browsershots database.
    """
    cur.close()
    con.commit()
    con.close()
    del __builtins__['cur']
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

        >>> Printer.execute('INSERT INTO test (a, b) VALUES (%(a)s, %(b)s)', {'a': 'ab\\'c%', 'b': 4, 'c': None})
        INSERT INTO test (a, b) VALUES ('ab\\'c%', 4)

        >>> Printer.execute('SELECT * FROM test WHERE a LIKE %s AND b = %s AND c IS %s', ('ab\\'c%', 4, None))
        SELECT * FROM test WHERE a LIKE 'ab\\'c%' AND b = 4 AND c IS NULL
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
    import sys, doctest
    cur = Printer()
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
