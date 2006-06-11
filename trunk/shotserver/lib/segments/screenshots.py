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
Display recent screenshots for a given website.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database

def write():
    """
    Write XHTML div with recent screenshots.
    """
    database.connect()
    try:
        xhtml.write_open_tag_line('div', _id="screenshots")
        now = time.time()
        rows = req.params.show_screenshots
        for index, row in enumerate(rows):
            hashkey, browser, major, minor, platform, created = row
            prefix = hashkey[:2]
            if index == 0:
                xhtml.write_open_tag_line('div', _class="screenshot first")
            else:
                xhtml.write_open_tag_line('div', _class="screenshot")
            xhtml.write_tag('img', src="/png/140/%s/%s.png" % (prefix, hashkey))

            # xhtml.write_tag_line('br')
            # req.write(time.strftime('%b %d %H:%M', time.localtime(created)))

            xhtml.write_tag_line('br')
            browser = database.browser.browser_version(browser, major, minor)
            req.write('%s on %s' % (browser, platform))

            xhtml.write_tag_line('br')
            req.write('%s ago' % human.timespan(now - created, units='long'))
            xhtml.write_tag_line('br')

            xhtml.write_close_tag_line('div') # class="screenshot"
        xhtml.write_tag_line('div', '', _class="clear")
        xhtml.write_close_tag_line('div') # id="screenshots"
    finally:
        database.disconnect()
