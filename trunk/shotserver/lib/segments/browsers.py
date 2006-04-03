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
Display available browsers with major and minor version number, grouped by platform.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml
from shotserver03 import database

def select_browsers(platform, where):
    cur.execute("""SELECT browser.name, browser_version.major, browser_version.minor
        FROM factory_browser
        JOIN factory USING (factory)
        JOIN os_version USING (os_version)
        JOIN os USING (os)
        JOIN browser_version USING (browser_version)
        JOIN browser USING (browser)
        WHERE %s
        ORDER BY browser.name, browser_version.major, browser_version.minor""" % where)
    result = []
    for row in cur.fetchall():
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
    
def write_header(platforms):
    xhtml.write_open_tag('tr')
    for platform in platforms:
        xhtml.write_tag('th', platform)
    xhtml.write_close_tag_line('tr')

def write_columns(*columns):
    row = 0
    while True:
        cells = []
        done = True
        for column in columns:
            if len(column) > row:
                cell = column[row]
                done = False
            else:
                cell = ''
            cells.append(xhtml.tag('td', cell))
        if done:
            break
        xhtml.write_tag_line('tr', ''.join(cells))
        row += 1

def write():
    database.connect()
    try:
        linux = select_browsers('linux', "os.name = 'Linux' AND NOT browser.terminal AND NOT os_version.mobile")
        mac = select_browsers('mac', "os.name = 'Mac OS' AND NOT browser.terminal AND NOT os_version.mobile")
        windows = select_browsers('windows', "os.name = 'Windows' AND NOT browser.terminal AND NOT os_version.mobile")
        terminal = select_browsers('terminal', "browser.terminal AND NOT os_version.mobile")
        mobile = select_browsers('mobile', "os_version.mobile")
    finally:
        database.disconnect()

    xhtml.write_open_tag_line('table', _id="browsers")
    write_header('Linux Mac Windows Terminal Mobile'.split())
    write_columns(linux, mac, windows, terminal, mobile)
    xhtml.write_close_tag_line('table') # id="browsers"
