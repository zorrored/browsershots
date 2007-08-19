# browsershots.org ShotServer 0.3-beta1
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
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
Show all queued requests for a given website.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database


def optionstring(group_row):
    """
    Convert some options to a human-readable string.
    """
    dummy, width, bpp, js, java, flash, media, dummy, dummy = group_row
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


def write_requests(requests, opsys_dict):
    """
    Write a summary of the queuing requests for a give request group.
    """
    platforms = {}
    for request_row in requests:
        browser, major, minor, opsys = request_row
        if opsys is not None:
            opsys = opsys_dict[opsys]
        platform = platforms.get(opsys, [])
        platform.append(database.browser.version_string(browser, major, minor))
        platforms[opsys] = platform
    keys = platforms.keys()
    keys.sort()
    if keys[0] is None:
        keys.append(keys.pop(0))
    xhtml.write_open_tag_line('ul', _class="up")
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
        groups = req.params.show_queue
        xhtml.write_open_tag_line('div', _id="queue")
        for index, group_row in enumerate(groups):
            group = group_row[0]
            requests = database.request.select_by_group(group)
            if not requests:
                continue
            submitted, expire = group_row[-2:]
            age = human.timespan(time.time() - submitted, units='long')
            remaining = human.timespan(expire - time.time(), units='long')
            if time.time() - submitted < 30 and index == len(groups) - 1:
                xhtml.write_open_tag('p', _class="success")
                xhtml.write_tag('a', xhtml.tag('b', 'Just submitted'),
                                id_="success")
            else:
                xhtml.write_open_tag('p')
                xhtml.write_tag('b', 'Submitted %s ago' % age)
            req.write(', to expire in %s' % remaining)
            options = optionstring(group_row)
            if options:
                req.write(', with ' + options)
            xhtml.write_close_tag_line('p')
            write_requests(requests, opsys_dict)
        xhtml.write_close_tag_line('div') # id="queue"
    finally:
        database.disconnect()
