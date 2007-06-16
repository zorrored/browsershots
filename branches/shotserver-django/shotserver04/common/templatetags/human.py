# browsershots.org - Test your web design in different browsers
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
Convert times to a short human-readable format.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime
from django import template

register = template.Library()


@register.filter
def human_seconds(seconds):
    """
    >>> human_seconds(0)
    '0 s'
    >>> human_seconds(1)
    '1 s'
    >>> human_seconds(5*60)
    '5 min'
    >>> human_seconds(5*3600)
    '5 h'
    >>> human_seconds(5*24*3600)
    '5 d'
    """
    if seconds is None:
        return ''
    if seconds < 180:
        return _("%(seconds)d s") % locals()
    minutes = seconds / 60
    if minutes < 180:
        return _("%(minutes)d min") % locals()
    hours = minutes / 60
    if hours < 72:
        return _("%(hours)d h") % locals()
    days = hours / 24
    return _("%(days)d d") % locals()


@register.filter
def human_timesince(then):
    if then is None:
        return ''
    delta = datetime.now() - then
    return human_seconds(delta.days * 24 * 3600 + delta.seconds)


@register.filter
def human_bytes(bytes):
    """
    >>> human_bytes(0)
    '0 bytes'
    >>> human_bytes(100)
    '100 bytes'
    >>> human_bytes(9999)
    '9999 bytes'
    >>> human_bytes(10000)
    '10 000 bytes'
    >>> human_bytes(10000000)
    '10 000 000 bytes'
    >>> human_bytes(123456789)
    '123 456 789 bytes'
    """
    bytes = str(bytes)
    if len(bytes) > 4:
        for index in range(len(bytes) - 3, 0, -3):
            bytes = bytes[:index] + ' ' + bytes[index:]
    return _("%(bytes)s bytes") % locals()


@register.filter
def human_link(object):
    """
    HTML link to the detail page.
    """
    return '<a href="%s">%s</a>' % (object.get_absolute_url(), str(object))


@register.filter
def human_br(text):
    """
    Add <br /> tags for narrow table headers.

    >>> human_br('test')
    'test'
    >>> human_br('last upload')
    'last<br />upload'
    >>> human_br('browser-group')
    'browser-<br />group'
    >>> human_br('a b c d')
    'a b<br />c d'
    """
    middle = len(text) / 2
    candidates = []
    for index, char in enumerate(text):
        if char in ' -':
            candidates.append((abs(middle - index), index, char))
    candidates.sort()
    if not candidates:
        return text
    middle, index, char = candidates[0]
    if char == '-':
        return text[:index+1] + '<br />' + text[index+1:]
    else:
        return text[:index] + '<br />' + text[index+1:]


@register.filter
def human_datetime(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    import doctest
    _ = lambda x: x
    doctest.testmod()
