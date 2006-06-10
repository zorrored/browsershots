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
Database interface for website table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

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
    cur.execute("SELECT website FROM website WHERE url=%s", (url, ))
    row = cur.fetchone()
    return row[0]
