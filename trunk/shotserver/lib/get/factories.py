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

from shotserver03.interface import xhtml
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
        cur.execute("""SELECT factory.name, opsys.name, distro, major, minor, codename
            FROM factory
            JOIN opsys_version USING (opsys_version)
            JOIN opsys USING (opsys)
            ORDER BY opsys.name, major, minor, factory.name
            """)
        result = cur.fetchall()
    finally:
        database.disconnect()

    xhtml.write_open_tag_line('table')
    for name, opsys, distro, major, minor, codename in result:
        xhtml.write_open_tag('tr')
        xhtml.write_tag('td', name)
        if distro is not None:
            opsys = '%s %s' % (opsys, distro)
        opsys = database.opsys.version_string(opsys, major, minor, codename)
        xhtml.write_tag('td', opsys)
        xhtml.write_close_tag_line('tr')
    xhtml.write_close_tag_line('table')
