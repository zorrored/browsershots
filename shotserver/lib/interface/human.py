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
Output formatting for human consumption.
>>> __builtins__.req = sys.stdout
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def cutoff(text, maxlen):
    """
    Shorten a string if necessary, trying to cut at space.
    Up to <maxlen> characters of the original string will be preserved.
    >>> cutoff('abc', 3)
    'abc'
    >>> cutoff('abcd', 3)
    'abc...'
    >>> cutoff('a bc', 3)
    'a ...'
    >>> cutoff('ab cd', 3)
    'ab ...'
    >>> cutoff('abc de', 3)
    'abc...'
    >>> cutoff('abcd ef', 3)
    'abc...'
    """
    if len(text) <= maxlen:
        return text
    cut = text.rfind(' ', 0, maxlen)
    if cut == -1:
        cut = maxlen
    else:
        cut += 1
    return text[:cut] + '...'

def write_table_rows(obj, prefix = ''):
    """
    Debug instance variables in XHTML table rows.
    """
    keys = obj.__dict__.keys()
    keys.sort()
    for key in keys:
        value = obj.__dict__[key]
        if hasattr(value, '__dict__'):
            write_table_rows(value, prefix + key + '.')
        else:
            value = str(value)
            value = value.replace('<', '&lt;')
            value = value.replace('>', '&gt;')
            xhtml.write_tag_line('tr',
                xhtml.tag('th', prefix + key + ':') +
                xhtml.tag('td', value))

def write_table(obj, prefix = ''):
    """
    Debug instance variables with XHTML table.
    >>> write_table(p, 'p.')
    <table>
    <tr><th>p.name:</th><td>abc</td></tr>
    <tr><th>p.sub.x:</th><td>42</td></tr>
    </table>
    """
    xhtml.write_open_tag_line('table')
    write_table_rows(obj, prefix)
    xhtml.write_close_tag_line('table')

if __name__ == '__main__':
    import sys, doctest
    from shotserver03.request import params
    p = params.Params()
    p.name = 'abc'
    p.sub = params.Params()
    p.sub.x = 42
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
