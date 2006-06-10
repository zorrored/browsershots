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
Display recent screenshots in a horizontal row.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import random
from shotserver03.interface import xhtml

max_thumbs = 12

def write():
    """
    Write XHTML div with recent screenshots.
    """
    xhtml.write_open_tag_line('div', _id="recent")

    lines = file('/var/www/browsershots.org/png/sizes.txt').readlines()
    random.shuffle(lines)
    for index, line in enumerate(lines):
        if index == max_thumbs:
            break
        image, width, height = line.split()
        width = int(width) / 2
        height = int(height) / 2
        style = "right:%dpx;width:%dpx;height:%dpx;margin-right:-30px;z-index:1" % (30 + index * 64, width/2, height/2)
        img = xhtml.tag('img', src='/'.join(('', 'png', '120', image)), alt="", _class="absolute",
                        onmouseover="larger(this,%d,%d)" % (width, height),
                        onmouseout="smaller(this,%d,%d)" % (width, height),
                        style=style)
        xhtml.write_tag_line('a', img, href='png/240/%s' % image)

    xhtml.write_close_tag_line('div') # id="recent"
    xhtml.write_tag_line('div', '', _class="spacer", style="height:140px;margin:0 0 1em")
