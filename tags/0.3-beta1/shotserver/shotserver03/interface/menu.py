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
XHTML formatting for simple menus.
>>> __builtins__.req = sys.stdout
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml


def write(_class, items):
    """
    Write XHTML <ul> with menu entries.
    >>> write('testmenu', ('Home=/', ))
    <ul class="testmenu"><li class="first"><a href="/">Home</a></li></ul>
    """
    xhtml.write_open_tag('ul', _class=_class)
    for index, item in enumerate(items):
        text, link = item.split('=', 1)
        if index == 0:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link),
                            class_="first")
        else:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link))
    xhtml.write_close_tag_line('ul') # class="float-right"

if __name__ == '__main__':
    import sys
    import doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
