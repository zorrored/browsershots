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
Output formatting for human consumption.
>>> __builtins__.req = sys.stdout
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

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


def timespan(seconds, rounding = "", units = ""):
    """
    Format a time span in seconds to human-readable text.
    Specify rounding = "up" or "down" if you don't want to round correctly.

    >>> timespan(1), timespan(1, units = "long")
    ('1 s', '1 seconds')
    >>> timespan(120), timespan(120, units = "long")
    ('2 min', '2 minutes')
    >>> timespan(2 * 60 * 60), timespan(2 * 60 * 60, units = "long")
    ('2 h', '2 hours')
    >>> timespan(6 * 24 * 60 * 60), timespan(6 * 24 * 60 * 60, units = "long")
    ('6 d', '6 days')
    >>> timespan(140 * 24 * 60 * 60), timespan(12096000, units = "long")
    ('20 w', '20 weeks')
    >>> timespan(3650 * 24 * 60 * 60), timespan(315360000, units = "long")
    ('10 y', '10 years')

    >>> timespan(119, rounding = "up"), timespan(119, rounding = "down")
    ('2 min', '1 min')
    >>> timespan(120, rounding = "up"), timespan(120, rounding = "down")
    ('2 min', '2 min')
    >>> timespan(121, rounding = "up"), timespan(121, rounding = "down")
    ('3 min', '2 min')
    """
    round_add = (3, 12, 30, 182)
    if rounding == "up":
        round_add = (6, 23, 59, 364)
    if rounding == "down":
        round_add = (0, 0, 0, 0)

    sec_string = "%d s"
    min_string = "%d min"
    hour_string = "%d h"
    day_string = "%d d"
    week_string = "%d w"
    year_string = "%d y"
    if units == "long":
        sec_string = "%d seconds"
        min_string = "%d minutes"
        hour_string = "%d hours"
        day_string = "%d days"
        week_string = "%d weeks"
        year_string = "%d years"

    if seconds < 100:
        return sec_string % seconds
    minutes = (seconds + round_add[2]) / 60
    if minutes < 100:
        return min_string % minutes
    hours = (minutes + round_add[2]) / 60
    if hours < 100:
        return hour_string % hours
    days = (hours + round_add[1]) / 24
    if days < 100:
        return day_string % days
    weeks = (days + round_add[0]) / 7
    if weeks < 100:
        return week_string % weeks
    years = (days + round_add[3]) / 365
    return year_string % years

if __name__ == '__main__':
    import sys
    import doctest
    from shotserver03.request import params
    p = params.Params()
    p.name = 'abc'
    p.sub = params.Params()
    p.sub.x = 42
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
