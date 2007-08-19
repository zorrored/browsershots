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
Show the latest news headlines from the blog.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
import re
import time
from shotserver03.interface import xhtml, human

rss_filename = '/var/www/browsershots.org/blog/rss.xml'
find_items = re.compile(r'<item>\s*' +
                        r'<title>(.+?)</title>\s*' +
                        r'<pubDate>(.+?)</pubDate>\s*' +
                        r'<link>(http.+?)</link>',
                        re.IGNORECASE).findall


def write():
    """
    Write XHTML div with latest news headlines.
    """
    xhtml.write_open_tag_line('div', _id="news")
    link = xhtml.tag('a', "Latest News",
                     href='http://trac.browsershots.org/blog')
    xhtml.write_tag_line('h2', link)

    if not os.path.exists(rss_filename):
        xhtml.write_tag('p', 'File %s not found.' % rss_filename)
        xhtml.write_close_tag_line('div') # id="news"
        return

    xhtml.write_open_tag_line('ul')
    rss = file(rss_filename).read()
    items = find_items(rss)
    if len(items) > 10:
        items = items[:10]
    for item in items:
        title, pubdate, link = item
        date = time.strptime(pubdate, '%a, %d %b %Y %H:%M:%S GMT')
        date = time.strftime('%Y-%m-%d', date)
        date = xhtml.tag('span', date, class_="news-date")
        title = human.cutoff(title, 36)
        link = xhtml.tag('a', title, href=link)
        xhtml.write_tag_line('li', '%s %s' % (link, date))
    xhtml.write_close_tag_line('ul')

    xhtml.write_close_tag_line('div') # id="news"


if __name__ == '__main__':
    import sys

    class writer:
        """Simple writer class for testing from command line."""

        def __init__(self):
            self.write = sys.stdout.write

    __builtins__.req = writer()
    write()
