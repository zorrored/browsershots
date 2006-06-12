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
Drop-down boxes for browser features.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write_select(name, options, selected = None):
    """
    Write XHTML drop-down input.
    """
    xhtml.write_open_tag_line('select', _name=name)
    for index, option in enumerate(options.split('|')):
        value, text = option.split('=')
        if selected and index == selected - 1:
            xhtml.write_tag_line('option', text, value=value, selected="selected")
        else:
            xhtml.write_tag_line('option', text, value=value)
    xhtml.write_close_tag_line('select')

def write():
    """
    Write drop-down boxes for browser features.
    """
    xhtml.write_open_tag_line('div', _class="gray background", _id="features")

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Screen resolution")
    xhtml.write_tag_line('br')
    write_select('width', "dontcare=Don't Care|640=Tiny (640x480)|800=Small (800x600)|1024=Medium (1024x768)" +
                 "|1280=Large (1280x1024)|1600=Huge (1600x1200)")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "JavaScript")
    xhtml.write_tag_line('br')
    write_select('js', "dontcare=Don't Care|no=Disabled|yes=Enabled|1.3=Version 1.3|1.4=Version 1.4|" +
                 "1.5=Version 1.5|1.6=Version 1.6")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Macromedia Flash")
    xhtml.write_tag_line('br')
    write_select('flash', "dontcare=Don't Care|no=Not Installed|yes=Installed|4=Version 4|5=Version 5|6=Version 6" +
                 "|7=Version 7|8=Version 8")
    xhtml.write_close_tag_line('div')

    # If jobs can't be finished soon enough, they will be removed from the queue.
    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Maximum wait")
    xhtml.write_tag_line('br')
    write_select('expire', "0:15=15 minutes|0:30=30 minutes|1:00=1 hour|2:00=2 hours|4:00=4 hours", 2)
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Color depth")
    xhtml.write_tag_line('br')
    write_select('bpp', "dontcare=Don't Care|4=4 Bits (16 Colors)|8=8 Bits (256 Colors)|" +
                 "16=16 Bits (High Color)|24=24 Bits (True Color)")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Java")
    xhtml.write_tag_line('br')
    write_select('java', "dontcare=Don't Care|no=Not Installed|yes=Installed|blackdown=Blackdown|kaffe=Kaffe" +
                 "|sun=Sun Java|sun_1.2=Sun Java 1.2|sun_1.3=Sun Java 1.3|sun_1.4=Sun Java 1.4|sun_5.0=Sun Java 5.0")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Media plugins")
    xhtml.write_tag_line('br')
    write_select('media', "dontcare=Don't Care|quicktime=Apple Quicktime|wmp=Windows Media Player|svg=SVG|pdf=PDF")
    xhtml.write_close_tag_line('div')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="features"
