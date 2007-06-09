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
Websites.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def extract_domain(url, remove_www=False):
    """
    Extract domain name from URL, without user, password, or port.

    >>> extract_domain('http://www.example.com')
    'www.example.com'
    >>> extract_domain('http://www.example.com/')
    'www.example.com'
    >>> extract_domain('http://www.example.com/index.html')
    'www.example.com'
    >>> extract_domain('http://www.example.com:8000')
    'www.example.com'
    >>> extract_domain('http://user:password@www.example.com:8000')
    'www.example.com'
    >>> extract_domain('http://www.example.com', remove_www=True)
    'example.com'
    >>> extract_domain('http://www.www.example.com', remove_www=True)
    'example.com'
    >>> extract_domain('www.example.com')
    'www.example.com'
    """
    # Remove http:// and /index.html
    if url.count('/') >= 2:
        domain = url.split('/')[2]
    else:
        domain = url.strip('/')
    # Remove user:password@
    if domain.count('@'):
        domain = domain.split('@')[1]
    # Remove port (e.g. :8000)
    if domain.count(':'):
        domain = domain.split(':')[0]
    # Remove www. if requested
    while domain.startswith('www.') and remove_www:
        domain = domain[4:]
    return domain


if __name__ == '__main__':
    import doctest
    doctest.testmod()
