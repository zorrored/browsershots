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
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import random
import base64

SECRET_KEY_DEFAULT_LENGTH = 512


def random_chars(length):
    """
    Generate a random bitstring.

    >>> len(random_chars(123))
    123
    >>> min(random_chars(10000))
    '\\x00'
    >>> max(random_chars(10000))
    '\\xff'
    """
    chars = []
    for index in range(length):
        if index % 23 == 0:
            random.seed()
        chars.append(chr(random.randint(0, 255)))
    return ''.join(chars)


def random_secret_key(length=SECRET_KEY_DEFAULT_LENGTH):
    """
    Generate a random base64-encoded string.

    >>> len(random_secret_key()) == SECRET_KEY_DEFAULT_LENGTH
    True
    >>> len(random_secret_key(4))
    4
    >>> len(random_secret_key(1024))
    1024
    >>> random_secret_key(5)
    Traceback (most recent call last):
    ...
    AssertionError
    """
    assert length % 4 == 0
    return base64.b64encode(random_chars(length / 4 * 3))


def random_hash_key():
    """
    Generate a random MD5-like key.

    >>> len(random_hash_key())
    32
    >>> min(random_hash_key() + random_hash_key() + random_hash_key())
    '0'
    >>> max(random_hash_key() + random_hash_key() + random_hash_key())
    'f'
    """
    return random_chars(16).encode('hex')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
