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
from shotserver03 import database

def select_browsers(platform, where):
    """
    Select available browsers from database.
    Return a list of XHTML checkbox elements,
    one for each browser, one for all.
    """
    result = []
    for row in database.factory_browser.active_browsers(where):
        browser, major, minor = row
        code = '%s_%s_%d_%d' % (platform, browser.lower(), major, minor)
        result.append(
            xhtml.tag('input', _type="checkbox", _id=code, _name=code, checked="checked",
                onclick="updateMaster('%s')" % platform) + ' ' +
            xhtml.tag('label', '%s %d.%d' % (browser, major, minor), _for=code))
    code = '%s_all' % platform
    result.append(
        xhtml.tag('input', _type="checkbox", _id=code, checked="checked",
            onclick="multiCheck('%s',this.checked)" % platform) + ' ' +
        xhtml.tag('label', '<b>All</b>', _for=code))
    return result

def write_float(platform, browsers, columns):
    """
    Write browser list for one platform.
    """
    per_column = len(browsers) / columns
    if len(browsers) % columns:
        per_column += 1
    for column in range(columns):
        xhtml.write_open_tag_line('div', _class="float-left")
        if column == 0:
            xhtml.write_tag('b', platform)
        xhtml.write_tag_line('br')
        start = column * per_column
        stop = start + per_column
        if stop > len(browsers):
            stop = len(browsers)
        for index in range(start, stop):
            req.write(browsers[index])
            xhtml.write_tag_line('br')
        xhtml.write_close_tag_line('div') # id="browsers"

def write():
    """
    Write browser selection form.
    """
    xhtml.write_open_tag_line('div', _id="browsers", _class="blue background")
    database.connect()
    try:
        linux = select_browsers('linux', "opsys_group.name = 'Linux' AND NOT browser_group.terminal AND NOT opsys.mobile")
        mac = select_browsers('mac', "opsys_group.name = 'Mac OS' AND NOT browser_group.terminal AND NOT opsys.mobile")
        windows = select_browsers('windows', "opsys_group.name = 'Windows' AND NOT browser_group.terminal AND NOT opsys.mobile")
        terminal = select_browsers('Terminal', "browser_group.terminal AND NOT opsys.mobile")
        mobile = select_browsers('Mobile', "opsys.mobile")
    finally:
        database.disconnect()

    columns = []
    if len(linux) > 1:
        columns.append([len(linux), 'Linux', linux, 1])
    if len(mac) > 1:
        columns.append([len(mac), 'Mac', mac, 1])
    if len(windows) > 1:
        columns.append([len(windows), 'Windows', windows, 1])
    if len(terminal) > 1:
        columns.append([len(terminal), 'Terminal', terminal, 1])
    if len(mobile) > 1:
        columns.append([len(mobile), 'Mobile', mobile, 1])

    used = len(columns)
    while used < 5:
        columns.sort()
        longest = columns[-1]
        longest[-1] += 1
        longest[0] = len(longest[2]) / longest[-1]
        used += 1

    columns.sort()
    columns.reverse()
    for column in columns:
        write_float(column[1], column[2], column[3])

    xhtml.write_tag_line('input', _type="submit", _id="submit", _name="submit", value="Submit Jobs", _class="button")
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="browsers"
