# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Helper functions for the systems app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver05.xmlrpc.utils import import_method


def signature(method_name):
    method = import_method(method_name)
    lines = method.__doc__.splitlines()
    index = 0
    while index < len(lines) and lines[index].strip() != 'Arguments:':
        index += 1
    index += 1
    if index < len(lines):
        assert lines[index].strip() == '~~~~~~~~~~'
    index += 1
    arguments = []
    while index < len(lines) and lines[index].strip().startswith('*'):
        arguments.append(lines[index].split()[2])
        index += 1
    if index >= len(lines):
        index = 0
    while index < len(lines) and lines[index].strip() != 'Return value:':
        index += 1
    index += 1
    if index < len(lines):
        assert lines[index].strip() == '~~~~~~~~~~~~~'
    index += 1
    return_values = []
    while index < len(lines) and lines[index].strip().startswith('*'):
        return_values.append(lines[index].split()[2])
        index += 1
    if len(return_values) < 1:
        return_values = ['string']
    if len(return_values) > 1:
        return_values = ['list']
    return return_values + arguments
