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
    for row_index, row in enumerate(rows):
        hashkey, width, height, url = row
        height = height * 140 / width
        width = 140
        if row_index > 5 and height > (len(rows) - row_index) * 28:
            continue
        minimum = min(columns)
        smallest = columns.index(minimum)
        left = 156 * smallest
        top = columns[smallest]
        columns[smallest] += height + 16
        prefix = hashkey[:2]
        img = xhtml.tag('img', alt="Screenshot of %s" % url, title=url,
                        src='/png/140/%s/%s.png' % (prefix, hashkey),
                        width=width, height=height,
                        style="left:%dpx;top:%dpx;" % (left, top))
        xhtml.write_tag_line('a', img, href='/png/full/%s/%s.png' % (prefix, hashkey))
    xhtml.write_tag_line('div', '&nbsp;', style="height:%dpx;" % max(columns))
    xhtml.write_close_tag_line('div') # id="screenshots"
