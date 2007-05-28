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
Screenshot factory authentication.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03 import database

export_methods = ['challenge', 'test']


def challenge(factory):
    """
    challenge(string) => string
    Generate a random authentication challenge.
    Parameter:
    - The name of the factory (string, length max 20).
    Return value:
    - Authentication challenge (hex string, length 36).
      The first 4 characters contain the password salt.
      The remaining 32 characters contain a random nonce.
    """
    database.connect()
    try:
        try:
            factory = database.factory.name_to_serial(factory)
        except KeyError:
            return "Unknown factory name '%s'." % factory
        salt = database.factory.select_salt(factory)
        ip = req.connection.remote_ip
        nonce = database.nonce.create_factory_nonce(factory, ip)
        return salt + nonce
    finally:
        database.disconnect()


def test(factory, crypt):
    """
    test(string, string) => string
    Test factory authentication.
    Parameters:
    - The name of the factory (string, length max 20).
    - Crypted password (hex string, length 32):
      crypt = md5(md5(salt + password) + nonce)
    Return value:
    - String 'OK' or error message.
    """
    database.connect()
    try:
        try:
            factory = database.factory.name_to_serial(factory)
        except KeyError:
            return "Unknown factory name '%s'." % factory
        ip = req.connection.remote_ip
        return database.nonce.authenticate_factory(factory, ip, crypt)
    finally:
        database.disconnect()
