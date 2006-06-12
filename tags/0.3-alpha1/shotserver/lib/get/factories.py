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
List all factories.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import time
from shotserver03.interface import xhtml, human
from shotserver03 import database

def title():
    """Return page title."""
    return "Screenshot Factories"

def body():
    """
    Write HTML page content.
    """
    database.connect()
    try:
        rows = database.factory.select_active()
    finally:
        database.disconnect()

    now = time.time()
    xhtml.write_open_tag_line('table')
    xhtml.write_table_row(("Name", "Operating System", "Last poll", "Last upload"), element="th")
    for row in rows:
        name, opsys, distro, major, minor, codename, last_poll, last_upload = row
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', name)
        opsys = database.opsys.version_string(opsys, distro, major, minor, codename)
        xhtml.write_tag('td', opsys)
        if last_poll is None:
            xhtml.write_tag('td', "never")
        else:
            xhtml.write_tag('td', human.timespan(now - last_poll))
        if last_upload is None:
            xhtml.write_tag('td', "never")
        else:
            xhtml.write_tag('td', human.timespan(now - last_upload))
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
