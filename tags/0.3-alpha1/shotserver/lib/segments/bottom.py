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
Display bottom line with some links.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml, menu

def write():
    """
    Write bottom menu.
    """
    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_open_tag_line('div', _class="menu lightgray", _id="bottom")

    menu.write('float-left', (
        "Contact=http://trac.browsershots.org/wiki/ContactDetails",
        "Terms of Use=http://trac.browsershots.org/wiki/TermsOfUse",
        "Privacy Policy=http://trac.browsershots.org/wiki/PrivacyPolicy"))

    menu.write('float-right', (
        "XHTML 1.1=http://validator.w3.org/check?uri=referer",
        "CSS=http://jigsaw.w3.org/css-validator/check/referer"))

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="bottom"
