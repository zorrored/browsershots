# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
XML-RPC methods for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver05.xmlrpc.utils import user_auth


@user_auth
def testAuth(request, user, dummy_number, dummy_text):
    """
    Test user authentication with MD5 hash. To compute the hash,
    concatenate the string values of all the other arguments and the
    pre-hashed user password, then get the MD5 hash as 32 lowercase
    hexadecimal characters. If the username is 'joe' and the
    pre-hashed password is 'sha1$e3$4d07f85', you might get the
    following MD5 hash:

    >>> md5('123hello2008-08-08T23:56:14Zjoesha1$e3$4d07f85').hexdigest()
    '2eb594e041eeb418e86ef0289328ed1c'

    Arguments:
    ~~~~~~~~~~
    * username string (e.g. joe)
    * dummy_number int (e.g. 123)
    * dummy_text string (e.g. hello)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    return 'OK'
