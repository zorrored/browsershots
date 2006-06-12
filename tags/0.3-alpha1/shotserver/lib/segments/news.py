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
Show the latest news headlines from the blog.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import re
from shotserver03.interface import xhtml, human

items = re.compile('<item>\s*<title>(.+?)</title>\s*<link>(http.+?)</link>').findall
def write():
    """
    Write XHTML div with latest news headlines.
    """
    xhtml.write_open_tag_line('div', _id="news")
    xhtml.write_tag_line('h2', "Latest News")

    xhtml.write_open_tag_line('ul')
    rss = file('/var/www/browsershots.org/blog/rss.xml').read()
    for item in items(rss):
        title, link = item
        title = human.cutoff(title, 36)
        link = xhtml.tag('a', title, href=link)
        xhtml.write_tag_line('li', link)
    xhtml.write_close_tag_line('ul')

    xhtml.write_close_tag_line('div') # id="news"
