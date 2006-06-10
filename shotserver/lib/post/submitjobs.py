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
Add new screenshot jobs to the queue.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

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

screen_width = {'tiny': 640, 'small': 800, 'medium': 1024, 'large': 1280, 'huge': 1600}
terminal_width = {'tiny': 50, 'small': 64, 'medium': 80, 'large': 132, 'huge': 168}

def insert_requests(website, browsers, features):
    """
    Insert screenshot requests into database.
    """
    values = {}
    values['website'] = website
    for key in 'bpp js java flash media expire'.split():
        if features[key] == 'dontcare':
            values[key] = None
        else:
            values[key] = features[key]
    for key in 'bpp expire'.split():
        if values[key] is not None:
            values[key] = int(values[key])
    request_group = database.request.insert_group(values)

    browser_int = database.browser.get_name_dict()
    opsys_int = database.opsys.get_name_dict()

    for platform, browser, major, minor in browsers:
        values = {}
        values['request_group'] = request_group
        values['browser_group'] = browser_int[browser]
        values['major'] = int(major)
        values['minor'] = int(minor)
        if platform == 'terminal':
            values['width'] = terminal_width[features['width']]
        elif platform == 'mobile':
            values['width'] = None
        else:
            values['width'] = screen_width[features['width']]
            values['opsys'] = opsys_int[platform]
        database.insert('request', values)


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
        insert_requests(website, browsers, features)
    finally:
        database.disconnect()
    util.redirect(req, '/website/%d/' % website)

    # sanity_check_url(url)
    # test_head(url)
    # website = select_or_insert(url)
