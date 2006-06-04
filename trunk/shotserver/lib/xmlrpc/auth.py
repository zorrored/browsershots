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
Screenshot factory authentication.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03 import database

export_methods = ['get_nonce']

def get_nonce(factory):
    """
    get_nonce(string) => string
    Get a pseudo-random authorization token (128 bits hexadecimal).
    The first parameter is the name of the factory.
    """
    database.connect()
    try:
        factory = database.factory.select_serial(factory)
        nonce = database.nonce.create_factory_nonce(factory, req.connection.remote_ip)
    finally:
        database.disconnect()
    return nonce
