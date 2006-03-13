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
Home page.
"""

__revision__ = '$Rev: 882 $'
__date__ = '$Date: 2005-12-31 15:20:50 +0100 (Sa, 31 Dez 2005) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml

def title():
    return "Welcome"

def body():
    xhtml.write_tag_line('p', 'Hello')
