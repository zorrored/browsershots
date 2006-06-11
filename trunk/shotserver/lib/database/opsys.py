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
Database interface for opsys table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def get_name_dict():
    """
    Get a mapping from lowercase operating system name to id (numeric primary key).
    """
    cur.execute('SELECT opsys_group, name FROM opsys_group')
    result = {}
    for opsys, name in cur.fetchall():
        if name == 'Mac OS':
            name = 'Mac'
        result[name.lower()] = opsys
    return result

def get_serial_dict():
    """
    Get a mapping from id (numeric primary key) to operating system name.
    """
    cur.execute('SELECT opsys_group, name FROM opsys_group')
    result = {}
    for opsys, name in cur.fetchall():
        if name == 'Mac OS':
            name = 'Mac'
        result[opsys] = name
    return result

def version_string(browser, major=None, minor=None, codename=None):
    """
    Make a string with browser name and version number.
    The version number parts will be skipped if None.
    """
    result = [browser]
    if major is not None:
        result.append(' %d' % major)
        if minor is not None:
            result.append('.%d' % minor)
    if codename is not None:
        result.append(' (%s)' % codename)
    return ''.join(result)
