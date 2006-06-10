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
Show all queued requests for a given website.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database

def optionstring(width, bpp, js, java, flash, media):
    """
    Convert some options to a human-readable string.
    """
    options = []
    if width is not None:
        options.append("%d pixels screen size" % width)
    if bpp is not None:
        options.append("%d bits per pixel" % bpp)
    if js is not None:
        options.append("JavaScript")
    if java is not None:
        options.append("Java")
    if flash is not None:
        options.append("Flash")
    if media is not None:
        if media == 'wmp':
            options.append("Windows Media Player")
        elif media == 'svg':
            options.append("Scalable Vector Graphics")
        else:
            options.append(media)
    if len(options) == 1:
        return options[0]
    elif len(options) > 1:
        last = options.pop()
        return ', '.join(options) + ' and ' + last


def write_requests(group, opsys_dict):
    """
    Write a summary of the queuing requests for a give request group.
    """
    requests = database.request.select_by_group(group)
    platforms = {}
    for request_row in requests:
        browser, major, minor, opsys = request_row
        if opsys is not None:
            opsys = opsys_dict[opsys]
        platform = platforms.get(opsys, [])
        platform.append('%s %d.%d' % (browser, major, minor))
        platforms[opsys] = platform
    keys = platforms.keys()
    keys.sort()
    if keys[0] is None:
        keys.append(keys.pop(0))
    xhtml.write_open_tag_line('ul', _class="queue")
    for key in keys:
        if key is None:
            platform = 'Others'
        else:
            platform = str(key)
        browsers = ', '.join(platforms[key])
        xhtml.write_tag_line('li', '%s: %s' % (platform, browsers))
    xhtml.write_close_tag_line('ul')

def write():
    """
    Write XHTML table with queued requests for a given website.
    """
    database.connect()
    try:
        opsys_dict = database.opsys.get_serial_dict()
        groups = database.request.select_by_website(req.params.website)
        for index, group_row in enumerate(groups):
            group, width, bpp, js, java, flash, media, submitted, expire = group_row

            age = human.timespan(time.time() - submitted, units='long')
            remaining = human.timespan(expire - time.time(), units='long')
            if time.time() - submitted < 30 and index == len(groups) - 1:
                xhtml.write_open_tag('p', _class="queue success")
                xhtml.write_tag('a', xhtml.tag('b', 'Just submitted'), _id="success")
            else:
                xhtml.write_open_tag('p', _class="queue")
                xhtml.write_tag('b', 'Submitted %s ago' % age)
            req.write(', to expire in %s' % remaining)
            options = optionstring(width, bpp, js, java, flash, media)
            if options:
                req.write(', with ' + options)
            xhtml.write_close_tag_line('p') # class="queue"
            write_requests(group, opsys_dict)
    finally:
        database.disconnect()
