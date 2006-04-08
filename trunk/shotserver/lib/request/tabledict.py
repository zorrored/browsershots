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
Store and debug HTTP request information.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

class TableDict:
    """
    Print instance variables in XHTML table rows.
    """

    def __init__(self):
        pass

    def write_table_rows(self, prefix = ''):
        """
        Debug instance variables in XHTML table rows.
        """
        keys = self.__dict__.keys()
        keys.sort()
        for key in keys:
            value = self.__dict__[key]
            if hasattr(value, 'write_table_rows'):
                value.write_table_rows(prefix + key + '.')
            else:
                value = str(value)
                value = value.replace('<', '&lt;')
                value = value.replace('>', '&gt;')
                xhtml.write_tag_line('tr',
                    xhtml.tag('th', prefix + key + ':') +
                    xhtml.tag('td', value))

    def write_table(self):
        """
        Debug instance variables with XHTML table.
        """
        xhtml.write_open_tag_line('table')
        self.write_table_rows()
        xhtml.write_close_tag_line('table')
