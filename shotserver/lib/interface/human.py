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
