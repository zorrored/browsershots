# -*- coding: utf-8 -*-
# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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
Display drop-down language selector.
"""

__revision__ = '$Rev: 41 $'
__date__ = '$Date: 2006-03-15 07:46:49 +0100 (Wed, 15 Mar 2006) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML form with drop-down language selector.
    """
    xhtml.write_open_tag_line('form', action="")
    xhtml.write_open_tag('div', _id="languages", _class="float-right")
    # xhtml.write_tag_line('input', _type="text")
    # xhtml.write_tag_line('input', _type="submit", value="Search")

    xhtml.write_open_tag_line('select', _id="langsel",
        onchange="document.location.href=this.form.langsel.options[this.form.langsel.options.selectedIndex].value")
    xhtml.write_tag_line('option', 'English', value="en")
    xhtml.write_tag_line('option', 'English (Canada)', value="en-CA")
    xhtml.write_tag_line('option', 'Deutsch', value="de")
    xhtml.write_tag_line('option', 'Português (Brazil)', value="pt-BR")
    xhtml.write_tag_line('option', 'Български', value="bg")
    xhtml.write_tag_line('option', '正體中文', value="zh")
    xhtml.write_close_tag_line('select')
    xhtml.write_close_tag_line('div') # id="languages"
    xhtml.write_close_tag_line('form')
