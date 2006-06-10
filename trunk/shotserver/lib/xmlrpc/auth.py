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
Screenshot factory authentication.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

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
        factory = database.factory.select_serial(factory)
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
        factory = database.factory.select_serial(factory)
        ip = req.connection.remote_ip
        return database.nonce.authenticate_factory(factory, ip, crypt)
    finally:
        database.disconnect()
