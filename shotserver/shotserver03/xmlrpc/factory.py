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
Factory configuration.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03 import database

export_methods = ['features']


def features(factory):
    """
    features(string) => string
    Generate an SQL WHERE clause that matches requests for a given factory.

    Parameter:
    - The name of the factory (string, length max 20).

    Return value:
    - SQL WHERE clause (string).
    """
    database.connect()
    try:
        factory = database.factory.name_to_serial(factory)
        return database.factory.features(factory)
    finally:
        database.disconnect()
