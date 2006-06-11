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
Database interface for browser table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def get_name_dict():
    """
    Get a mapping from lowercase browser name to id (numeric primary key).
    """
    cur.execute("SELECT browser_group, name FROM browser_group")
    result = {}
    for browser, name in cur.fetchall():
        result[name.lower()] = browser
    return result

def select_by_useragent(useragent):
    """
    Select the browser with a given User-Agent string.
    """
    cur.execute("""\
SELECT browser, browser_group, browser_group.name, major, minor
FROM browser
JOIN browser_group USING (browser_group)
WHERE useragent = %s
""", (useragent, ))
    return cur.fetchone()

def version_string(browser, major=None, minor=None):
    """
    Make a string with browser name and version number.
    The version number parts will be skipped if None.
    """
    result = [browser]
    if major is not None:
        result.append(' %d' % major)
        if minor is not None:
            result.append('.%d' % minor)
    return ''.join(result)
