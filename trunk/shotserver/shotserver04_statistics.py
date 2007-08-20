#!/usr/bin/env python
# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Collect statistics for ShotServer 0.4.

You should run this every few minutes, e.g. by adding the following
line in /etc/crontab (replace www-data with the database owner):

*/5 *   * * *   www-data   shotserver04_statistics.py
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import os
import fcntl

# Allow a single instance of this script only
LOCKFILENAME = os.path.join('/var/lock',
    os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.pid')
LOCKFILE = open(LOCKFILENAME, 'w')
try:
    fcntl.flock(LOCKFILE.fileno(), fcntl.LOCK_EX|fcntl.LOCK_NB)
except IOError, e:
    if e.errno == 11:
        sys.exit(1)
LOCKFILE.write(str(os.getpid()) + '\n')
LOCKFILE.truncate()

os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
from datetime import datetime, timedelta
from shotserver04 import settings
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.screenshots.models import Screenshot
from shotserver04.websites.models import Website
from shotserver04.websites.utils import count_profanities, http_get, HTTPError

ONE_HOUR_AGO = datetime.now() - timedelta(0, 3600, 0)
ONE_DAY_AGO = datetime.now() - timedelta(1, 0, 0)


for factory in Factory.objects.all():
    factory.uploads_per_hour = Screenshot.objects.filter(
        factory=factory, uploaded__gte=ONE_HOUR_AGO).count()
    factory.uploads_per_day = Screenshot.objects.filter(
        factory=factory, uploaded__gte=ONE_DAY_AGO).count()
    browsers = Browser.objects.filter(factory=factory)
    factory.save()
    for browser in browsers:
        browser.uploads_per_hour = Screenshot.objects.filter(
            browser=browser, uploaded__gte=ONE_HOUR_AGO).count()
        browser.uploads_per_day = Screenshot.objects.filter(
            browser=browser, uploaded__gte=ONE_DAY_AGO).count()
        browser.save()


if '--content' in sys.argv:
    for website in Website.objects.order_by('fetched')[:20]:
        print website.url
        try:
            website.content = http_get(website.url)
        except HTTPError:
            pass
        website.fetched = datetime.now()
        website.save()


if '--profanities' in sys.argv:
    for website in Website.objects.all():
        profanities = count_profanities(
            settings.PROFANITIES_LIST,
            ' '.join((website.url, website.content)))
        if website.profanities != profanities:
            website.profanities = profanities
            website.save()
