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
Add new screenshot jobs to the queue.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import urllib
from shotserver03 import database


class UnexpectedInput(Exception):
    """Post form input had unexpected fields."""
    pass

browser_match = re.compile(r'^(\w+)_([\w\-]+)_(\d+)_(\d+)$').match
expire_match = re.compile(r'^(\d+):(\d\d)$').match
url_match = re.compile(r'\w+://(www\.|)([\w\.\-]+)').match
feature_keys = 'width bpp js java flash media expire'.split()


def read_form(form):
    """
    Get known fields from post form.
    Raise UnexpectedInput if field name is not known.
    """
    url = ''
    browsers = []
    features = {}
    for key in form.keys():
        browser = browser_match(key)
        if key == 'url':
            url = form[key]
        elif key == 'submit':
            pass
        elif key in feature_keys:
            features[key] = form[key]
        elif browser:
            if form[key] == 'on':
                browsers.append(browser.groups())
        else:
            raise UnexpectedInput(key)
    return url, browsers, features


def error_redirect(**params):
    """
    Redirect back to website overview because an error has occurred.
    """
    from mod_python import util
    params = urllib.urlencode(params)
    if params:
        util.redirect(req, '/?' + params)
    else:
        util.redirect(req, '/')


def limit_expire(expire):
    """
    Upper limit on expiry interval.

    >>> limit_expire('invalid')
    '0:30'
    >>> limit_expire('2:00')
    '2:00'
    >>> limit_expire('2:61')
    '3:01'
    >>> limit_expire('4000:99')
    '4:00'
    >>> limit_expire('4:01')
    '4:00'
    """
    match = expire_match(expire)
    if not match:
        return '0:30'
    hours = int(match.group(1))
    minutes = int(match.group(2))
    if minutes > 59:
        hours += 1
        minutes -= 60
    if hours > 4 or (hours == 4 and minutes > 0):
        hours = 4
        minutes = 0
    return '%d:%02d' % (hours, minutes)


def extract_domain(url):
    """
    Extract the domain name from a http:// URL, without www prefix.

    >>> extract_domain('http://browsershots.org/submit/')
    'browsershots.org'
    >>> extract_domain('http://www.google.com')
    'google.com'
    >>> extract_domain('https://test.example.com:8000/')
    'test.example.com'
    """
    match = url_match(url)
    if match is None:
        raise ValueError(url)
    return match.group(2)


def insert_requests(website, browsers, features, priority):
    """
    Insert screenshot requests into database.
    """
    group_values = {}
    group_values['website'] = website
    for key in feature_keys:
        if features[key] == 'dontcare':
            group_values[key] = None
        else:
            group_values[key] = features[key]
    for key in 'width bpp'.split():
        if group_values[key] is not None:
            group_values[key] = int(group_values[key])
    old_groups = database.request.find_identical_groups(group_values)
    group_values['expire'] = limit_expire(group_values['expire'])
    request_group = database.request.insert_group(group_values)

    browser_int = database.browser.get_name_dict()
    opsys_int = database.opsys.get_name_dict()

    for platform, browser, major, minor in browsers:
        values = {}
        values['request_group'] = request_group
        values['browser_group'] = browser_int[browser]
        values['major'] = int(major)
        values['minor'] = int(minor)
        values['opsys_group'] = None
        values['priority'] = priority
        if platform not in ['terminal', 'mobile']:
            values['opsys_group'] = opsys_int[platform]
        if old_groups:
            database.request.delete_identical(values, old_groups)
        database.request.insert(values)


def redirect():
    """
    Insert new jobs into queue.
    Redirect to overview page on success.
    Redirect back to overview page on error.
    """
    url, browsers, features = read_form(req.info.form)
    database.connect()
    try:
        website = database.website.select_serial(url)
        assert website
        domain = extract_domain(url)
        priority = database.priority_domain.get_priority(domain)
        insert_requests(website, browsers, features, priority)
    finally:
        database.disconnect()
    from mod_python import util
    util.redirect(req, '/website/%d/#success' % website)

    # sanity_check_url(url)
    # test_head(url)
    # website = select_or_insert(url)

if __name__ == '__main__':
    import sys
    import doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
