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
Get browser details from user agent string.

Useful for default values when adding browsers in Django admin.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import threading

_thread_locals = threading.local()


def get_engines():
    """
    Get all rendering engines from the database.

    Make sure that KHTML and Gecko are returned last, because some
    browsers include those names in their User-Agent string, in
    addition to their real engine name.
    """
    from shotserver04.browsers.models import Engine
    khtml = gecko = None
    for engine in Engine.objects.all():
        if engine.name == 'Gecko':
            gecko = engine
        elif engine.name == 'KHTML':
            khtml = engine
        else:
            yield engine
    if khtml:
        yield khtml
    if gecko:
        yield gecko


def get_browser_groups():
    """
    Get all browser groups from the database.

    Make sure that Firefox and Mozilla are returned last, because
    other browsers include those names in their User-Agent string.
    """
    from shotserver04.browsers.models import BrowserGroup
    firefox = mozilla = None
    for browser_group in BrowserGroup.objects.all():
        if browser_group.name == 'Firefox':
            firefox = browser_group
        elif browser_group.name == 'Mozilla':
            mozilla = browser_group
        else:
            yield browser_group
    if firefox:
        yield firefox
    if mozilla:
        yield mozilla


def extract_version(user_agent, name):
    """
    Extract version string that comes after the name.

    >>> extract_version('Mozilla/5.0', 'Mozilla')
    '5.0'
    >>> extract_version('Mozilla/5.0 Gecko/20061201 Firefox/2.0.0.4', 'Gecko')
    '20061201'
    """
    index = user_agent.index(name)
    index += len(name)
    if user_agent[index] != '/':
        return ''
    index += 1
    start = index
    while index < len(user_agent) and user_agent[index] in '.0123456789':
        index += 1
    return user_agent[start:index]


def extract_major(version):
    """
    Extract major version number from version string.

    >>> extract_major('2.0.0.4')
    2
    >>> extract_major('2')
    2
    """
    if version.count('.'):
        return int(version.split('.')[0])
    elif version.isdigit():
        return int(version)


def extract_minor(version):
    """
    Extract minor version number from version string.

    >>> extract_minor('2.18')
    18
    >>> extract_minor('2.0.0.4')
    0
    """
    if version.count('.'):
        return int(version.split('.')[1])


class BrowserInfoMiddleware(object):
    """
    Middleware that saves browser details in thread local storage.
    """

    def process_request(self, request):
        """
        Grab browser details from request.
        """
        # Only for "Add browser" in Django admin
        if not '/browsers/browser/add/' in request.META['PATH_INFO']:
            return
        # Get user agent from request
        user_agent = request.META['HTTP_USER_AGENT']
        _thread_locals.user_agent = user_agent
        # Extract engine and engine version from user agent string
        for engine in get_engines():
            if engine.name in user_agent:
                _thread_locals.engine = engine
                version = extract_version(user_agent, engine.name)
                _thread_locals.engine_version = version
                break
        # Extract browser group and version from user agent string
        for browser_group in get_browser_groups():
            if browser_group.name in user_agent:
                _thread_locals.browser_group = browser_group
                version = extract_version(user_agent, browser_group.name)
                _thread_locals.version = version
                _thread_locals.major = extract_major(version)
                _thread_locals.minor = extract_minor(version)
                break


#########################################################################
# The following functions can be used as default entries for model fields
#########################################################################


def get_user_agent():
    """Get user agent of current browser."""
    return getattr(_thread_locals, 'user_agent', None)


def get_browser_group():
    """Get browser group id of current browser."""
    browser_group = getattr(_thread_locals, 'browser_group', None)
    if browser_group:
        return browser_group.id


def get_command():
    """Get default command of current browser."""
    browser_group = getattr(_thread_locals, 'browser_group', None)
    if browser_group:
        return browser_group.name.lower()


def get_version():
    """Get version string of current browser."""
    return getattr(_thread_locals, 'version', None)


def get_major():
    """Get major version number of current browser."""
    return getattr(_thread_locals, 'major', None)


def get_minor():
    """Get minor version number of current browser."""
    return getattr(_thread_locals, 'minor', None)


def get_engine():
    """Get engine id of current browser."""
    engine = getattr(_thread_locals, 'engine', None)
    if engine:
        return engine.id


def get_engine_version():
    """Get engine version of current browser."""
    return getattr(_thread_locals, 'engine_version', None)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
