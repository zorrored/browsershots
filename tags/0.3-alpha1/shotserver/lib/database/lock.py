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
