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
Display factories and some information in an XHTML table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('form', action="/post/submit/", method="post")

    xhtml.write_open_tag_line('p', _id="inputurl")
    xhtml.write_tag_line('input', _type="submit", _id="submit", _name="submit", value="Make Screenshots", _class="right")
    xhtml.write_tag_line('input', _type="text", _id="url", _name="url", value="Enter your web address here", size=50)
    xhtml.write_close_tag_line('p')

    xhtml.write_open_tag_line('table', _id="factories")
    
    xhtml.write_open_tag('tr')
    xhtml.write_tag('th', 'Browser name<br />and version', colspan=2)
    xhtml.write_tag('th', 'Rendering<br />engine')
    xhtml.write_tag('th', 'Operating<br />system')
    xhtml.write_tag('th', 'Last<br />poll')
    xhtml.write_tag('th', 'Last<br />upload')
    xhtml.write_tag('th', 'Uploads<br />in 24h')
    xhtml.write_tag('th', 'Jobs in<br />queue')
    xhtml.write_tag('th', 'Queue<br />time')
    xhtml.write_close_tag_line('tr')

    factories = [
        ('Epiphany 1.4.8', 'Gecko 20050718', 'Linux Debian', '4 min', '4 min', '233', '10', '62 minutes'),
        ('Firefox 1.0.4', 'Gecko 20050825', 'Linux Debian', '14 s', '46 s', '288', '15', '75 minutes'),
        ('Firefox 1.5.0', 'Gecko 20060224', 'Linux Ubuntu', '89 s', '3 min', '515', '19', '54 minutes'),
        ('Galeon 1.3.20', 'Gecko 20050718', 'Linux Debian', '2 min', '13 min', '233', '10', '62 minutes'),
        ('Konqueror 3.3', 'KHTML 3.3.2', 'Linux Debian', '8 min', '7 min', '242', '13', '78 minutes'),
        ('Mozilla 1.7.8', 'Gecko 20050718', 'Linux Debian', '5 min', '7 min', '235', '12', '74 minutes'),
        ('MSIE 6.0', 'MSIE 6.0', 'Windows XP SP2', '28 s', '85 s', '705', '18', '37 minutes'),
        ('MSIE 7.0 Beta', 'MSIE 7.0 Beta', 'Windows XP SP2', '13 s', '16 s', '342', '2', '9 minutes'),
        ('Opera 8.50', 'Opera 8.50', 'Linux Debian', '48 s', '64 s', '238', '9', '55 minutes'),
        ('Safari 2.0', 'KHTML', 'Mac OS X', '24 s', '25 s', '603', '17', '41 minutes'),
        ]

    for index, factory in enumerate(factories):
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', xhtml.tag('input', checked="checked", type="checkbox", value=str(index), _name="factory"))
        for column, cell in enumerate(factory):
            if cell.endswith('minutes') and cell[1] != ' ' and cell[0:2] > '60':
                cell = xhtml.tag('span', cell, _class="red")
            xhtml.write_tag('td', cell)
        xhtml.write_close_tag_line('tr')
        
    xhtml.write_close_tag_line('table') # id="factories"
    xhtml.write_close_tag_line('form')
