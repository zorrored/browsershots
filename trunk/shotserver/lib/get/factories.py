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
List all factories.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml, human
from shotserver03.segments import factory_list, factory_browsers
from shotserver03 import database as db

def read_params():
    """
    Read parameters from the request URL.
    """
    if len(req.info.options) == 1:
        factory = req.info.options[0]
        db.connect()
        try:
            if factory.isdigit():
                req.params.factory = factory
                req.params.factory_name = db.factory.select_name(factory)
            else:
                req.params.factory_name = factory
                req.params.factory = db.factory.select_serial(factory)
        finally:
            db.disconnect()

def title():
    """Return page title."""
    if hasattr(req.params, 'factory'):
        return "Screenshot Factory: %s" % req.params.factory_name
    else:
        return "Screenshot Factories"

def body():
    """
    Write HTML page content.
    """
    if hasattr(req.params, 'factory'):
        factory_browsers.write()
    else:
        factory_list.write()
