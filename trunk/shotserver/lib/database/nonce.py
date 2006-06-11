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
Database interface for nonce table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import md5, random, time, os

def random_md5():
    """
    Make a random 128bit hexadecimal authentication token.
    """
    digest = md5.new()
    digest.update('%.50f' % random.random())
    digest.update('%.20f' % time.time())
    digest.update(os.urandom(16))
    return digest.hexdigest()

def create_factory_nonce(factory, ip):
    """
    Make a factory nonce and save it in the database.
    """
    nonce = random_md5()
    cur.execute("INSERT INTO nonce (nonce, factory, ip) VALUES (%s, %s, %s)", (nonce, factory, ip))
    return nonce

def create_request_nonce(request, ip):
    """
    Make a factory nonce and save it in the database.
    """
    nonce = random_md5()
    cur.execute("INSERT INTO nonce (nonce, request, ip) VALUES (%s, %s, %s)", (nonce, request, ip))
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

def authenticate_redirect(ip, crypt):
    """
    Authenticate a redirect with a crypted password.
    The crypted password can be created with a nonce:
    salt = challenge[:4]
    nonce = challenge[4:]
    crypt = md5('redirect' + md5(salt + password) + nonce)
    """
    cur.execute("""\
SELECT url, request, browser_group, browser_group.name, major, minor FROM nonce
JOIN request USING (request)
JOIN request_group USING (request_group)
JOIN browser_group USING (browser_group)
JOIN website USING (website)
JOIN lock USING (request)
JOIN factory ON lock.factory = factory.factory
JOIN person AS owner ON factory.owner = owner.person
WHERE nonce.ip = %s
AND (md5('redirect' || factory.password || nonce.nonce) = %s
OR md5('redirect' || owner.password || nonce.nonce) = %s)
""", (ip, crypt, crypt))
    row = cur.fetchone()
    if row is None:
        return 'Password mismatch.', '', 0, 0, '', 0, 0
    else:
        url, request, group, name, major, minor = row
        return 'OK', url, request, group, name, major, minor

def authenticate_request(ip, crypt):
    """
    Authenticate a request with a crypted password.
    The crypted password can be created with a nonce:
    salt = challenge[:4]
    nonce = challenge[4:]
    crypt = md5(md5(salt + password) + nonce)
    """
    cur.execute("""\
SELECT nonce, request, width, factory.factory, browser FROM nonce
JOIN request USING (request)
JOIN request_group USING (request_group)
JOIN lock USING (request)
JOIN factory ON lock.factory = factory.factory
JOIN person AS owner ON factory.owner = owner.person
WHERE nonce.ip = %s
AND (md5(factory.password || nonce.nonce) = %s
OR md5(owner.password || nonce.nonce) = %s)
""", (ip, crypt, crypt))
    row = cur.fetchone()
    if row is None:
        return 'Password mismatch.', 0, 0, 0, 0
    else:
        nonce, request, width, factory, browser = row
        cur.execute("DELETE FROM nonce WHERE nonce = %s", (nonce, ))
        if cur.rowcount:
            return 'OK', request, width, factory, browser
        else:
            return 'Nonce expired.', 0, 0, 0, 0
