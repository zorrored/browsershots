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
Display available browsers with major and minor version number,
grouped by platform.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml
from shotserver03 import database


def is_old_version(browser, major, minor, rows):
    """
    Check if there is a newer version of the same browser. If there
    is, then this old version will not be selected by default, except
    for the few browsers in the first line of this function.
    """
    if browser in 'Firefox MSIE Safari SeaMonkey Epiphany'.split():
        return False
    for row in rows:
        if (row[0] != browser):
            continue
        if (row[1] < major):
            continue
        if (row[1] == major and row[2] <= minor):
            continue
        return True


def select_browsers(platform, where):
    """
    Select available browsers from database. Return a list of XHTML
    checkbox elements, one for each browser, one for all browsers
    together. Old versions of most browsers are unselected by default.
    """
    result = []
    rows = database.factory_browser.active_browsers(where)
    all_checked = True
    for row in rows:
        browser, major, minor = row
        code = '%s_%s_%d_%d' % (platform, browser.lower(), major, minor)
        if is_old_version(browser, major, minor, rows):
            checkbox = xhtml.tag('input', _type="checkbox", _id=code,
                _name=code, onclick="updateMaster('%s')" % platform)
            all_checked = False
        else:
            checkbox = xhtml.tag('input', _type="checkbox", _id=code,
                _name=code, onclick="updateMaster('%s')" % platform,
                checked="checked")
        result.append(checkbox + ' ' +
            xhtml.tag('label', '%s %d.%d' % (browser, major, minor),
                      _for=code))
    code = '%s_all' % platform
    if all_checked:
        checkbox = xhtml.tag('input', _type="checkbox", _id=code,
            onclick="multiCheck('%s',this.checked)" % platform,
            checked="checked")
    else:
        checkbox = xhtml.tag('input', _type="checkbox", _id=code,
            onclick="multiCheck('%s',this.checked)" % platform)
    if len(result) > 3:
        result.append(checkbox + ' ' +
            xhtml.tag('label', '<b>All</b>', _for=code))
    return result


def write_float(platform, browsers, columns, leftmost):
    """
    Write browser list for one platform.
    """
    per_column = len(browsers) / columns
    if len(browsers) % columns:
        per_column += 1
    for column in range(columns):
        if column == 0 and not leftmost:
            xhtml.write_open_tag_line('div', class_="float-left",
                style="border-left: 1px dotted white; padding-bottom: 8px;")
        else:
            xhtml.write_open_tag_line('div', class_="float-left")
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
        linux = select_browsers('linux', "opsys_group.name = 'Linux'" +
            " AND NOT browser_group.terminal AND NOT opsys.mobile")
        mac = select_browsers('mac', "opsys_group.name = 'Mac OS'" +
            " AND NOT browser_group.terminal AND NOT opsys.mobile")
        windows = select_browsers('windows', "opsys_group.name = 'Windows'" +
            " AND NOT browser_group.terminal AND NOT opsys.mobile")
        terminal = select_browsers('Terminal', "browser_group.terminal" +
                                   " AND NOT opsys.mobile")
        mobile = select_browsers('Mobile', "opsys.mobile")
    finally:
        database.disconnect()

    columns = []
    if len(linux):
        columns.append([len(linux), 'Linux', linux, 1])
    if len(mac):
        columns.append([len(mac), 'Mac', mac, 1])
    if len(windows):
        columns.append([len(windows), 'Windows', windows, 1])
    if len(terminal):
        columns.append([len(terminal), 'Terminal', terminal, 1])
    if len(mobile):
        columns.append([len(mobile), 'Mobile', mobile, 1])

    used = len(columns)
    while 0 < used < 5:
        columns.sort()
        longest = columns[-1]
        if longest[0] <= 5:
            break
        longest[-1] += 1
        longest[0] = float(len(longest[2])) / longest[-1]
        used += 1

    columns.sort()
    columns.reverse()
    leftmost = True
    for column in columns:
        write_float(column[1], column[2], column[3], leftmost)
        leftmost = False

    xhtml.write_tag_line('input', value="Submit Jobs", _class="button",
                         _type="submit", _id="submit", _name="submit")
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="browsers"
