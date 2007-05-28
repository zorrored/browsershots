# browsershots.org ShotServer 0.3-beta1
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
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
Display browsers that are installed on a factory.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml
from shotserver03 import database


def write_tr_th_td(th, td, color=None):
    """Write XHTML table row with <th> and <td>."""
    if color is None:
        xhtml.write_open_tag('tr')
    else:
        xhtml.write_open_tag('tr', _class="color%d" % color)
    xhtml.write_tag('th', th)
    xhtml.write_tag('td', td)
    xhtml.write_close_tag_line('tr')


def write():
    """
    Write XHTML table with browsers installed on req.params.factory.
    """
    database.connect()
    try:
        (name, opsys, distro, major, minor, codename, arch,
         created, creator) = database.factory.info(req.params.factory)
        xhtml.write_open_tag_line('table', _id="factory-info")
        write_tr_th_td('Operating System', database.opsys.version_string(
            opsys, distro, major, minor, codename), color=1)
        write_tr_th_td('Architecture', arch, color=2)
        write_tr_th_td('Created', created, color=1)
        write_tr_th_td('Administrator', creator, color=2)
        xhtml.write_close_tag_line('table')
    finally:
        database.disconnect()
