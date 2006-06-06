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
Screenshot request handling.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03 import database

export_methods = ['poll']

def poll(factory, crypt):
    """
    poll(string, string) => array
    Try to find a matching screenshot request for a given factory.
    If successful, the request will be locked for 5 minutes.
    Parameters:
    - The name of the factory (string, length max 20).
    - Crypted password (hex string, length 32):
      crypt = md5(md5(salt + password) + nonce)
    Return value:
    - Status: string 'OK' or error message.
    - URL: website address to be opened in the browser.
    - Browser name with major and minor version number.
    - Screen width (pixels).
    - Color depth (bits per pixel).
    - JavaScript version string.
    - Java version string.
    - Flash version string.
    - Media Player version string.
    """
    database.connect()
    try:
        factory = database.factory.select_serial(factory)
        ip = req.connection.remote_ip
        status = database.nonce.authenticate_factory(factory, ip, crypt)
        if status != 'OK':
            return status, '', '', 0, 0, '', '', '', ''
        where = database.factory.features(factory)
        found = database.request.match(where)
        if found is None:
            status = 'No matching request.'
            return status, '', '', 0, 0, '', '', '', ''
        else:
            major = found.pop(2)
            minor = found.pop(2)
            if major:
                found[1] += ' %d' % major
            if major and minor:
                found[1] += '.%d' % minor
            found.insert(0, 'OK')
            for index in range(3, 5):
                if found[index] == None:
                    found[index] = 0
            for index in range(5, 9):
                if found[index] == None:
                    found[index] = ''
            return found
    finally:
        database.disconnect()
