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
Add new screenshot jobs to the queue.
"""

__revision__ = '$Rev: 117 $'
__date__ = '$Date: 2006-04-08 08:51:18 +0200 (Sat, 08 Apr 2006) $'
__author__ = '$Author: johann $'

import re, urllib
from mod_python import util
from shotserver03 import database

class UnexpectedInput(Exception):
    """Post form input had unexpected fields."""
    pass

browser_match = re.compile(r'(\w+)_(\w+)_(\d+)_(\d+)$').match
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
    params = urllib.urlencode(params)
    if params:
        util.redirect(req, '/?' + params)
    else:
        util.redirect(req, '/')

def get_browser_mapping():
    cur.execute('SELECT browser, name FROM browser')
    result = {}
    for browser, name in cur.fetchall():
        result[name.lower()] = browser
    return result

def get_os_mapping():
    cur.execute('SELECT os, name FROM os')
    result = {}
    for os, name in cur.fetchall():
        if name == 'Mac OS':
            name = 'Mac'
        result[name.lower()] = os
    return result

screen_width = {'tiny': 640, 'small': 800, 'medium': 1024, 'large': 1280, 'huge': 1600}
terminal_width = {'tiny': 50, 'small': 64, 'medium': 80, 'large': 132, 'huge': 168}

def insert_requests(website, browsers, features):
    browser_int = get_browser_mapping()
    os_int = get_os_mapping()
    for platform, browser, major, minor in browsers:
        request = {}
        request['website'] = website
        request['browser'] = browser_int[browser]
        request['major'] = int(major)
        request['minor'] = int(minor)
        request['expire'] = int(features['expire']) * 60

        for key in 'bpp js java flash media'.split():
            if features[key] == 'dontcare':
                request[key] = None
            else:
                request[key] = features[key]

        for key in 'bpp'.split():
            if request[key] is not None:
                request[key] = int(request[key])

        if platform == 'terminal':
            request['width'] = terminal_width[features['width']]
            request['os'] = None
        elif platform == 'mobile':
            request['width'] = None
            request['os'] = None
        else:
            request['width'] = screen_width[features['width']]
            request['os'] = os_int[platform]

        keys = "website browser major minor os width bpp js java flash media expire".split()
        columns = ', '.join(keys)
        values = '%(' + ')s, %('.join(keys) + ')s'
        sql = "INSERT INTO request (%s) VALUES (%s)" % (columns, values)
        cur.execute(sql, request)


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
        insert_requests(website, browsers, features)
    finally:
        database.disconnect()
    util.redirect(req, '/website/%d/' % website)

    # sanity_check_url(url)
    # test_head(url)
    # website = select_or_insert(url)
