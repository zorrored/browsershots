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
URL input for submitting a new URL.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import cgi
from shotserver03.interface import xhtml

def write(url):
    """
    Write XHTML form for submitting a new URL.
    """
    xhtml.write_open_tag_line('form', action="/website/", method="post")
    xhtml.write_open_tag_line('div', _class="blue background", _id="inputurl")

    xhtml.write_open_tag_line('div', _class="float-left")
    xhtml.write_tag('b', "Paste your web address here, starting with http://")
    xhtml.write_tag_line('br')
    quoted_url = cgi.escape(url, quote = True)
    xhtml.write_tag('input', _type="text", _id="url", _name="url", value=quoted_url, _class="text")
    xhtml.write_close_tag_line('div')

    xhtml.write_open_tag_line('div', _class="float-left")
    req.write('<br />\n')
    xhtml.write_tag_line('input', _type="submit", _id="submit", _name="submit", value="Start", _class="button")
    xhtml.write_close_tag_line('div')

    xhtml.write_tag_line('div', '', _class="clear")
    xhtml.write_close_tag_line('div') # id="inputurl"
    xhtml.write_close_tag_line('form')
