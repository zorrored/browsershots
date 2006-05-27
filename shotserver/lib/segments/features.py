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
Submit new jobs to the queue.
"""

__revision__ = '$Rev: 41 $'
__date__ = '$Date: 2006-03-15 07:46:49 +0100 (Wed, 15 Mar 2006) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml

def write_select(name, options, selected = None):
    xhtml.write_open_tag_line('select', _name=name)
    for index, option in enumerate(options.split('|')):
        value, text = option.split('=')
        if selected and index == selected - 1:
            xhtml.write_tag_line('option', text, value=value, selected="selected")
        else:
            xhtml.write_tag_line('option', text, value=value)
    xhtml.write_close_tag_line('select')

def write():
    xhtml.write_open_tag_line('div', _class="gray background", _id="features")

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Screen resolution")
    xhtml.write_tag_line('br')
    write_select('screen_resolution', "tiny=Tiny (640x480)|small=Small (800x600)|medium=Medium (1024x768)" +
                 "|large=Large (1280x1024)|huge=Huge (1600x1200)", 3)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "JavaScript")
    xhtml.write_tag_line('br')
    write_select('javascript', "any=Don't Care|no=Disabled|yes=Enabled|1.3=Version 1.3|1.4=Version 1.4|" +
                 "1.5=Version 1.5|1.6=Version 1.6", 3)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Macromedia Flash")
    xhtml.write_tag_line('br')
    write_select('flash', "any=Don't Care|no=Not Installed|yes=Installed|4=Version 4|5=Version 5|6=Version 6" +
                 "|7=Version 7|8=Version 8", 3)
    xhtml.write_close_tag_line('div')

    # If jobs can't be finished soon enough, they will be removed from the queue.
    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Maximum wait")
    xhtml.write_tag_line('br')
    write_select('expire_minutes', "15=15 minutes|30=30 minutes|60=1 hour|120=2 hours|240=4 hours", 2)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Color depth")
    xhtml.write_tag_line('br')
    write_select('bits_per_pixel', "any=Don't Care|4=4 Bits (16 Colors)|8=8 Bits (256 Colors)|" +
                 "16=16 Bits (High Color)|24=24 Bits (True Color)")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Java")
    xhtml.write_tag_line('br')
    write_select('java', "any=Don't Care|no=Not Installed|yes=Installed|1.0=Version 1.0|1.1=Version 1.1" +
                 "|1.2=Version 1.2|1.3=Version 1.3|1.4=Version 1.4|5.0=Version 5.0")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Media Plugins")
    xhtml.write_tag_line('br')
    write_select('media', "any=Don't Care|quicktime=Apple Quicktime|wmp=Windows Media Player")
    xhtml.write_close_tag_line('div')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="features"

