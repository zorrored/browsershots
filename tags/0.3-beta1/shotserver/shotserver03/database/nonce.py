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
Database interface for nonce table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.util import md5nonce


def create_factory_nonce(factory, ip):
    """
    Make a factory nonce and save it in the database.
    """
    nonce = md5nonce.random_md5()
    cur.execute("""\
INSERT INTO nonce (nonce, factory, ip)
VALUES (%s, %s, %s)
""", (nonce, factory, ip))
    return nonce


def create_request_nonce(request, ip):
    """
    Make a factory nonce and save it in the database.
    """
    nonce = md5nonce.random_md5()
    cur.execute("""\
INSERT INTO nonce (nonce, request, ip)
VALUES (%s, %s, %s)
""", (nonce, request, ip))
    return nonce


def authenticate_factory(factory, ip, crypt):
    """
    Authenticate a factory with a crypted password.
    The crypted password can be created with a challenge:
    salt = challenge[:4]
    nonce = challenge[4:]
    crypt = md5(md5(salt + password) + nonce)
    """
    cur.execute("""\
SELECT nonce FROM nonce
JOIN factory USING (factory)
JOIN person AS owner ON factory.owner = owner.person
WHERE nonce.factory = %s AND nonce.ip = %s
AND (md5(textcat(factory.password, nonce.nonce)) = %s
OR md5(textcat(owner.password, nonce.nonce)) = %s)
""", (factory, ip, crypt, crypt))
    result = cur.fetchone()
    if result is None:
        return 'Password mismatch.'
    else:
        nonce = result[0]
        cur.execute("DELETE FROM nonce WHERE nonce = %s", (nonce, ))
        if cur.rowcount:
            return 'OK'
        else:
            return 'Nonce expired.'


def authenticate_redirect(crypt, request=None):
    """
    Authenticate a redirect with a crypted password.

    The crypted password can be created with a nonce:
    salt = challenge[:4]
    nonce = challenge[4:]
    crypt = md5('redirect' + md5(salt + password) + nonce)

    If the request is spefied, the select will go much faster because
    it doesn't have to try MD5 on all factory and admin passwords.
    """
    where = ["(%s)" % ' OR '.join((
        "md5('redirect' || factory.password || nonce.nonce) = %s",
        "md5('redirect' || owner.password || nonce.nonce) = %s",
        ))]
    if request is not None:
        where.append('request = %d' % request)
    cur.execute("""\
SELECT url, request, browser_group.name, major, minor, request.factory
FROM nonce
JOIN request USING (request)
JOIN request_group USING (request_group)
JOIN browser_group USING (browser_group)
JOIN website USING (website)
JOIN factory ON factory.factory = request.factory
JOIN person AS owner ON factory.owner = owner.person
WHERE """ + ' AND '.join(where), (crypt, crypt))
    row = cur.fetchone()
    if row is None:
        return 'Password mismatch.', '', 0, '', 0, 0, 0
    else:
        url, request, name, major, minor, factory = row
        return 'OK', url, request, name, major, minor, factory


def authenticate_request(ip, crypt):
    """
    Authenticate a request with a crypted password.
    The crypted password can be created with a nonce:
    salt = challenge[:4]
    nonce = challenge[4:]
    crypt = md5(md5(salt + password) + nonce)
    """
    cur.execute("""\
SELECT nonce, request, width, factory.factory, factory_browser
FROM nonce
JOIN request USING (request)
JOIN request_group USING (request_group)
JOIN factory ON factory.factory = request.factory
JOIN person AS owner ON factory.owner = owner.person
WHERE nonce.ip = %s
AND (md5(factory.password || nonce.nonce) = %s
OR md5(owner.password || nonce.nonce) = %s)
""", (ip, crypt, crypt))
    row = cur.fetchone()
    if row is None:
        return 'Password mismatch.', 0, 0, 0, 0
    else:
        nonce, request, width, factory, factory_browser = row
        cur.execute("DELETE FROM nonce WHERE nonce = %s", (nonce, ))
        if cur.rowcount:
            return 'OK', request, width, factory, factory_browser
        else:
            return 'Nonce expired.', 0, 0, 0, 0
