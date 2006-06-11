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
Database interface for useragent table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def select_serial(header, insert = False):
    """
    Get the serial number from the database.
    If the useragent is not found and the insert parameter is set to True,
    insert it into database and try again.
    """
    cur.execute("SELECT useragent FROM useragent WHERE header=%s", (header, ))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    if not insert:
        return None
    cur.execute("INSERT INTO useragent (header) VALUES (%s)", (header, ))
    cur.execute("SELECT lastval()")
    row = cur.fetchone()
    return row[0]
