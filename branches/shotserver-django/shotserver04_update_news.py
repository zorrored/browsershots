#!/usr/bin/env python
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
Update news items from RSS feed.

You can run this manually or with a cronjob, e.g. by adding the following
line in /etc/crontab (replace www-data with the database owner):

23 *   * * *   www-data   shotserver04_update_news.py
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
import sys
import re
import time
import urllib2
from shotserver04 import settings
from shotserver04.start.models import NewsItem

find_items = re.compile(
    r'<item>\s*' +
    r'<title>(.+?)</title>\s*' +
    r'<pubDate>(.+?)</pubDate>\s*' +
    r'<link>(http.+?)</link>',
    re.IGNORECASE).findall

updated = []
rss = urllib2.urlopen('http://trac.browsershots.org/blog?format=rss').read()
for title, pubdate, url in find_items(rss):
    timetuple = time.strptime(pubdate, '%a, %d %b %Y %H:%M:%S %Z')
    date = '%04d-%02d-%02d' % timetuple[:3]
    print pubdate
    print timetuple
    print date
    print title
    print url
    print
    item, created = NewsItem.objects.get_or_create(
        url=url, defaults={'date': date, 'title': title})
    if item.date != date or item.title != title:
        item.date = date
        item.title = title
        item.save()
    updated.append(item.id)
NewsItem.objects.exclude(id__in=updated).delete()
