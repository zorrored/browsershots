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
Database interface for person table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import md5
from shotserver03.util import md5nonce
from shotserver03.util import md5crypt


def select_nickname(serial):
    """
    Get the nickname from the database.
    """
    cur.execute("SELECT nickname FROM person WHERE person=%s", (serial, ))
    result = cur.fetchone()
    if result is None:
        return None
    return result[0]


def select_serial(nickname):
    """
    Get the serial number from the database.
    """
    cur.execute("SELECT person FROM person WHERE nickname=%s", (nickname, ))
    result = cur.fetchone()
    if result is None:
        return None
    return result[0]


def insert(fields):
    """
    Insert a new user into the database.
    """
    salt = md5nonce.random_md5()
    salt4 = salt[:4]
    salt8 = salt[-8:]
    password = fields['password']
    fields['salt'] = salt4
    fields['password'] = md5.md5(salt4 + password).hexdigest()
    fields['htpasswd'] = md5crypt.md5crypt(password, salt8, '$apr1$')
    cur.execute("""\
INSERT INTO person
(name, email, nickname, salt, password, htpasswd)
VALUES (%(fullname)s, %(email)s, %(username)s, %(salt)s,
        %(password)s, %(htpasswd)s)
""", fields)
    cur.execute("SELECT lastval()")
    row = cur.fetchone()
    return row[0]
