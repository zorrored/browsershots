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
Display project sponsor logos with links.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML div with sponsor logos.
    """
    xhtml.write_open_tag_line('div', _id="sponsors")
    xhtml.write_tag_line('h2', "Sponsors")

    img = xhtml.tag('img', src="/style/mfg40.png", alt="MFG Stiftung BW", _class="top")
    link = xhtml.tag('a', img, href="http://www.mfg.de/stiftung/")
    xhtml.write_tag_line('p', link)

    img = xhtml.tag('img', src="/style/lisog40.png", alt="LiSoG e.V.", _class="top")
    link = xhtml.tag('a', img, href="http://www.lisog.org/")
    xhtml.write_tag_line('p', link)

    xhtml.write_close_tag_line('div') # id="sponsors"
