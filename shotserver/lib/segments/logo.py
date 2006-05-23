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
Show the project logo.
"""

__revision__ = '$Rev: 161 $'
__date__ = '$Date: 2006-05-20 22:52:43 +0200 (Sat, 20 May 2006) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml

def write():
    xhtml.write_open_tag_line('div', _id="logo")
    xhtml.write_tag_line('img', src="/style/logo40.png", _class="logo", alt="browsershots.org")
    xhtml.write_close_tag_line('div')
