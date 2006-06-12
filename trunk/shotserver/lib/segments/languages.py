# -*- coding: utf-8 -*-
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
Display drop-down language selector.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML form with drop-down language selector.
    """
    xhtml.write_open_tag_line('form', action="")
    xhtml.write_open_tag_line('div', _id="languages", _class="float-right")

    parts = ("document.location.href='/intl/'",
             "this.form.langsel.options[this.form.langsel.options.selectedIndex].value",
             "document.location.pathname")
    xhtml.write_open_tag_line('select', _id="langsel", onchange='+'.join(parts))
    xhtml.write_tag_line('option', 'English', value="en")
    xhtml.write_tag_line('option', 'English (Canada)', value="en-CA")
    xhtml.write_tag_line('option', 'Deutsch', value="de")
    xhtml.write_tag_line('option', 'Português (Brazil)', value="pt-BR")
    xhtml.write_tag_line('option', 'Български', value="bg")
    xhtml.write_tag_line('option', '正體中文', value="zh")
    xhtml.write_close_tag_line('select')
    xhtml.write_close_tag_line('div') # id="languages"
    xhtml.write_close_tag_line('form')
