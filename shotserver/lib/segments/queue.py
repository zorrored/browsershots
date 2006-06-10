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

def optionstring(bpp, js, java, flash, media):
    """
    Convert some options to a human-readable string.
    """
    options = []
    if bpp is not None:
        options.append("%d BPP" % bpp)
    if js is not None:
        options.append("JavaScript")
    if java is not None:
        options.append("Java")
    if flash is not None:
        options.append("Flash")
    if media is not None:
        if media == 'wmp':
            options.append("Windows Media Player")
        else:
            options.append(media)
    if len(options) == 1:
        return options[0]
    elif len(options) > 1:
        last = options.pop()
        return ', '.join(options) + ' and ' + last

def write():
    """
    Write XHTML table with queued requests for a given website.
    """
    database.connect()
    try:
        groups = database.request.select_by_website(req.params.website)
        for index, group_row in enumerate(groups):
            group, bpp, js, java, flash, media, submitted, expire = group_row

            age = human.timespan(time.time() - submitted, units='long')
            remaining = human.timespan(expire - time.time(), units='long')
            if time.time() - submitted < 10 and index == 0:
                xhtml.write_open_tag('p', _class="queue success")
            else:
                xhtml.write_open_tag('p', _class="queue")

            xhtml.write_tag('b', 'Requested %s ago' % age)
            req.write(', to expire in %s' % remaining)
            options = optionstring(bpp, js, java, flash, media)
            if options:
                req.write(', with ' + options)

            requests = database.request.select_by_group(group)
            platforms = {}
            for request_row in requests:
                browser, major, minor, opsys = request_row
                platform = platforms.get(opsys, [])
                platform.append('%s %d.%d' % (browser, major, minor))
                platforms[opsys] = platform
            for key, value in platforms.iteritems():
                xhtml.write_tag_line('br')
                if key is None:
                    platform = 'Others'
                else:
                    platform = str(key)
                browsers = ', '.join(value)
                req.write('\n%s: %s' % (platform, browsers))
            xhtml.write_close_tag_line('p') # class="queue"
    finally:
        database.disconnect()
