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
Database interface for opsys table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def get_name_dict():
    """
    Get a mapping from lowercase operating system name to id
    (numeric primary key).
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


def version_string(opsys, distro=None, major=None, minor=None, codename=None):
    """
    Make a string with browser name and version number.
    The version number parts will be skipped if None.
    """
    result = [opsys]
    if distro is not None:
        result.append(' %s' % distro)
    if major is not None:
        result.append(' %d' % major)
        if minor is not None:
            result.append('.%d' % minor)
    if codename is not None:
        result.append(' (%s)' % codename)
    return ''.join(result)
