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
List queued screenshot requests.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import cgi
from shotserver03.interface import xhtml
from shotserver03.segments import prevnext, medium, recent
from shotserver03 import database

def read_params():
    """
    Read parameters from the request URL.
    """
    if len(req.info.options) == 0:
        req.params.hashkey = None
    elif len(req.info.options) == 1:
        database.connect()
        try:
            req.params.hashkey = req.info.options[0]
            row = database.screenshot.select_by_hashkey(req.params.hashkey)
            if row is None:
                req.params.hashkey = None
            else:
                (req.params.screenshot, req.params.factory, req.params.browser,
                 req.params.width, req.params.height, req.params.created,
                 req.params.website, req.params.url) = row
                req.params.escaped = cgi.escape(req.params.url, True)
        finally:
            database.disconnect()

def title():
    """Return page title."""
    return "Recent Screenshots"

def body():
    """
    Write HTML page content.
    """
    if req.params.hashkey:
        bold = xhtml.tag('b', 'for ' + req.params.escaped)
        xhtml.write_tag_line('p', bold, _class="up")
        prevnext.write('prev')
        medium.write()
        prevnext.write('next')
    else:
        recent.write()
