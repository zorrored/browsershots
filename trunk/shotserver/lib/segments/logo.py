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
Show the project logo.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML div for project logo.
    """
    xhtml.write_open_tag_line('div', _id="logo")
    img = xhtml.tag('img', src="/style/logo40.png", _class="logo", alt="browsershots.org")
    xhtml.write_tag_line('a', img, href="http://%s/" % req.hostname)
    xhtml.write_close_tag_line('div')
