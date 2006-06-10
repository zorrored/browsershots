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
XHTML formatting for simple menus.
>>> __builtins__.req = sys.stdout
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write(_class, items):
    """
    Write XHTML <ul> with menu entries.
    >>> write('testmenu', ('Home=/', 'Test=test.html'))
    <ul class="testmenu"><li class="first"><a href="/">Home</a></li><li><a href="test.html">Test</a></li></ul>
    """
    xhtml.write_open_tag('ul', _class=_class)
    for index, item in enumerate(items):
        text, link = item.split('=', 1)
        if index == 0:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link), _class="first")
        else:
            xhtml.write_tag('li', xhtml.tag('a', text, href=link))
    xhtml.write_close_tag_line('ul') # class="float-right"

if __name__ == '__main__':
    import sys, doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
