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
Home page.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml
from shotserver03.segments import inputurl, about, news, sponsors

def title():
    """Page title."""
    return "Test your web design in different browsers"

class UnexpectedFieldName(Exception):
    """The posted input contained an unexpected field name."""
    pass

def read_form():
    """
    Read the posted input.
    """
    result = {}
    accept_fields = 'error url'.split()
    for name in accept_fields:
        result[name] = ''
    for field in req.info.form.list:
        if field.name not in accept_fields:
            raise UnexpectedFieldName(field.name)
        result[field.name] = field.value
    return result

def body():
    """
    Write the front page.
    """
    url = ''
    if req.info.form:
        parameters = read_form()
        if (parameters['error']):
            xhtml.write_tag('p', parameters['error'], _class="error")
        if (parameters['url']):
            url = parameters['url']
    inputurl.write(url)

    about.write()
    news.write()
    sponsors.write()
