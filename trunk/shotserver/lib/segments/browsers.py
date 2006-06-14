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
    """
    Select available browsers from database.
    Return a list of XHTML checkbox elements,
    one for each browser, one for all.
    """
    cur.execute("""\
SELECT DISTINCT browser_group.name, browser.major, browser.minor
FROM factory_browser
JOIN factory USING (factory)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN browser USING (browser)
JOIN browser_group USING (browser_group)
WHERE %s
ORDER BY browser_group.name, browser.major, browser.minor
""" % where)
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

def write_float(platform, where):
    """
    Write browser list for one platform.
    """
    browsers = select_browsers(platform.lower(), where)
    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', platform)
    xhtml.write_tag_line('br')
    for browser in browsers:
        req.write(browser)
        xhtml.write_tag_line('br')
    xhtml.write_close_tag_line('div') # id="browsers"

def write():
    """
    Write browser selection form.
    """
    xhtml.write_open_tag_line('div', _id="browsers", _class="blue background")
    database.connect()
    try:
        write_float('Linux', "opsys_group.name = 'Linux' AND NOT browser_group.terminal AND NOT opsys.mobile")
        write_float('Mac', "opsys_group.name = 'Mac OS' AND NOT browser_group.terminal AND NOT opsys.mobile")
        write_float('Windows', "opsys_group.name = 'Windows' AND NOT browser_group.terminal AND NOT opsys.mobile")
        write_float('Terminal', "browser_group.terminal AND NOT opsys.mobile")
        write_float('Mobile', "opsys.mobile")
    finally:
        database.disconnect()
    xhtml.write_tag_line('input', _type="submit", _id="submit", _name="submit", value="Submit Jobs", _class="button")
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="browsers"
