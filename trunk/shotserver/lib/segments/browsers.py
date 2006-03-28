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
Display available browsers with major and minor version number, grouped by platform.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('table', _id="browsers")

    xhtml.write_open_tag('tr')
    xhtml.write_tag('th', 'Linux')
    xhtml.write_tag('th', 'Mac')
    xhtml.write_tag('th', 'Windows')
    xhtml.write_tag('th', 'Text Based')
    xhtml.write_tag('th', 'Handheld')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Epiphany 1.4')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Camino 1.0')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Firefox 1.5')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Links 1.0')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Opera 8.5')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Firefox 1.0')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' MSIE 5.2')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' MSIE 5.5')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Lynx 2.8')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Palm 2.0')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Firefox 1.5')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Safari 1.2')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' MSIE 6.0')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' W3M 0.5')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Palm 3.0')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Galeon 1.3')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Safari 2.0')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' MSIE 7.0')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Konqueror 3.3')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Opera 8.5')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Mozilla 1.7')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_close_tag_line('tr')

    xhtml.write_open_tag('tr')
    xhtml.write_tag('td', xhtml.tag('input', _type="checkbox", checked="checked") + ' Opera 8.5')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_tag('td', '')
    xhtml.write_close_tag_line('tr')

    xhtml.write_close_tag_line('table') # id="browsers"
