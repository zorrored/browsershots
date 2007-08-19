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
Display recent screenshots for a given website.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import time
from shotserver03.interface import xhtml, human


def write():
    """
    Write XHTML div with recent screenshots.
    """
    xhtml.write_open_tag_line('div', _id="screenshots")
    now = time.time()
    rows = req.params.show_screenshots
    for index, row in enumerate(rows):
        hashkey, browser, version, platform, created = row
        prefix = hashkey[:2]
        if index == 0:
            xhtml.write_open_tag_line('div', _class="screenshot first")
        else:
            xhtml.write_open_tag_line('div', _class="screenshot")
        img = xhtml.tag('img', alt="", width="140",
                        src="/png/140/%s/%s.png" % (prefix, hashkey))
        xhtml.write_tag('a', img, href="/screenshots/%s/" % hashkey)

        # xhtml.write_tag_line('br')
        # req.write(time.strftime('%b %d %H:%M', time.localtime(created)))

        xhtml.write_tag_line('br')
        req.write('%s %s on %s' % (browser, version, platform))

        timespan = human.timespan(now - created, units='long')
        timespan = timespan.replace(' ', '&nbsp;')
        req.write(', %s ago' % timespan)
        xhtml.write_tag_line('br')

        xhtml.write_close_tag_line('div') # class="screenshot"
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="screenshots"
