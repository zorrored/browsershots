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
List queued screenshot requests.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml
from shotserver03 import database

def title():
    """Return page title."""
    return "Recent Screenshots"

def body():
    """
    Write HTML page content.
    """
    database.connect()
    try:
        rows = database.screenshot.select_recent()
    finally:
        database.disconnect()

    columns = [0] * 5
    xhtml.write_open_tag_line('div', _id="screenshots", _class="relative")
    for row in rows:
        smallest = 0
        minimum = columns[0]
        for index in range(1, 5):
            if columns[index] < minimum:
                minimum = columns[index]
                smallest = index
        hashkey, width, height, url = row
        height = height * 140 / width
        width = 140
        left = 156 * smallest
        top = columns[smallest]
        prefix = hashkey[:2]
        png_full = '/png/full/%s/%s.png' % (prefix, hashkey)
        png_140 = '/png/140/%s/%s.png' % (prefix, hashkey)
        img = xhtml.tag('img', alt="Screenshot of %s" % url, title=url,
                        src=png_140, width=width, height=height,
                        style="left:%dpx;top:%dpx;" % (left, top))
        columns[smallest] += height + 16
        xhtml.write_tag_line('a', img, href=png_full)
    largest = 0
    maximum = columns[0]
    for index in range(1, 5):
        if columns[index] > maximum:
            maximum = columns[index]
            largest = index
    xhtml.write_tag_line('div', '&nbsp;', style="height:%dpx;" % maximum)
    xhtml.write_close_tag_line('div') # id="screenshots"
