# browsershots.org - Test your web design in different browsers
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
XML-RPC interface for nonces app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from xmlrpclib import Fault
from shotserver04.xmlrpc import register
from shotserver04.common import get_or_fault
from shotserver04.nonces import crypto
from shotserver04.nonces.models import Nonce
from shotserver04.factories.models import Factory
from datetime import datetime, timedelta


@register(str, str)
def challenge(request, factory_name):
    """
    Generate a nonce for authentication.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)

    Return value
    ~~~~~~~~~~~~
    * challenge string (algorithm$salt$nonce)

    The return value is a string that contains the password encryption
    algorithm (sha1 or md5), the salt, and the nonce, separated by '$'
    signs, for example::

        sha1$0c0ac$eb403b48ec9bf887ba645408acad17a5

    See nonces.verify for how to encrypt your password with the nonce.
    """
    factory = get_or_fault(Factory, name=factory_name)
    hashkey = crypto.random_md5()
    ip = request.META['REMOTE_ADDR']
    Nonce.objects.create(factory=factory, hashkey=hashkey, ip=ip)
    password = factory.admin.password
    if password.count('$'):
        algo, salt, encrypted = password.split('$')
    else:
        algo, salt, encrypted = 'md5', '', password
    return '$'.join((algo, salt, hashkey))


@register(None, str, str)
def verify(request, factory_name, encrypted_password):
    """
    Test authentication with an encrypted password.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)
    * encrypted_password string (lowercase hexadecimal, length 32)

    Return value
    ~~~~~~~~~~~~
    * success boolean (or XML-RPC fault with error message)

    Password encryption
    ~~~~~~~~~~~~~~~~~~~
    To encrypt the password, you must first generate a nonce and get
    the encryption algorithm and salt (see nonces.challenge). Then you
    can compute the encrypted password like this::

        encrypted_password = md5(sha1(salt + password) + nonce)

    If requested by the challenge, you must use md5 rather than sha1
    for the inner hash. The result of each hash function call must be
    formatted as lowercase hexadecimal. The calls to nonces.challenge
    and nonces.verify must be made from the same IP address.
    """
    # Shortcut for use with other XML-RPC methods
    if isinstance(factory_name, Factory):
        factory = factory_name
    else:
        factory = get_or_fault(Factory, name=factory_name)
    ip = request.META['REMOTE_ADDR']
    # Get password hash from database
    password = factory.admin.password
    if password.count('$'):
        algo, salt, hashed = password.split('$')
    else:
        algo, salt, hashed = 'md5', '', password
    # Get matching nonces
    nonces = Nonce.objects.filter(factory=factory, ip=ip).extra(
        where=["MD5(%s || hashkey) = %s"],
        params=[hashed, encrypted_password])
    if len(nonces) == 0:
        raise Fault(0, 'Password mismatch.')
    if len(nonces) > 1:
        raise Fault(0, 'Hash collision.')
    # Check nonce freshness
    nonce = nonces[0]
    if datetime.now() - nonce.created > timedelta(0, 600, 0):
        nonce.delete()
        raise Fault(0, 'Nonce expired.')
    # Success!
    nonce.delete()
    return True
