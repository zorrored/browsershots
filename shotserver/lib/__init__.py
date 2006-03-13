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
Top-level shotserver module.
All HTTP requests are handled from here.
"""

__revision__ = '$Rev$'
__date__     = '$Date$'
__author__   = '$Author$'

import sys, traceback
from mod_python import apache
from interface import xhtml, menu

def import_deep(name):
    """
    Import a module from some.levels.deep and return the module
    itself, not its uppermost parent.
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def import_action(name):
    """Import an action module."""
    return import_deep("shotserver03.actions." + name)

def action_option(module, key, default):
    if hasattr(module, key):
        return module.__dict__[key]()
    else:
        return default

def write_html_head(title):
    req.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"')
    req.write(' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    xhtml.write_open_tag_line('html', xmlns="http://www.w3.org/1999/xhtml")

    xhtml.write_open_tag_line('head')
    xhtml.write_tag_line('title', '%s - Browsershots' % title)
    xhtml.write_tag_line('link', rel="stylesheet", type="text/css", href="/style/style.css")
    xhtml.write_close_tag_line('head')

def handler(req):
    """
    Process all incoming HTTP requests.
    """
    naked = False
    try:
        req.status = apache.OK
        req.content_type = 'application/xhtml+xml; charset=UTF-8'
        __builtins__['req'] = req

        # req.info = request.RequestInfo()
        action_module = import_action('start') # req.info.action
        naked = action_option(action_module, 'naked', False)
        title = action_option(action_module, 'title', 'Browsershots')
        write_html_head(title)

        xhtml.write_open_tag_line('body')
        xhtml.write_open_tag_line('div', _id="all")

        menu.write_top()
        xhtml.write_open_tag_line('div', _class="menu", _id="sub")
        xhtml.write_tag_line('img', src="style/logo40.png", _class="right")

        xhtml.write_open_tag('ul', _class="left")
        xhtml.write_tag('li', xhtml.tag('a', 'Screenshots', href="/screenshots/"), _class="first")
        xhtml.write_tag('li', xhtml.tag('a', 'Submit', href="/submit/"))
        xhtml.write_tag('li', xhtml.tag('a', 'Search', href="/search/"))
        xhtml.write_close_tag_line('ul') # class="left"

        xhtml.write_tag_line('h1', title)
        xhtml.write_close_tag_line('div') # id="sub"

        menu.write_bottom()
        menu.write_sponsors()

        xhtml.write_close_tag_line('div') # id="all"
        xhtml.write_close_tag_line('body')
        xhtml.write_close_tag_line('html')
        return req.status
    except:
        if naked == 'redirect':
            write_html_head()

        while len(xhtml.open_tags) > 2:
            xhtml.write_close_tag_line()
        if xhtml.open_tags[-1] == 'head':
            xhtml.write_close_tag_line('head')
        if xhtml.open_tags[-1] != 'body':
            xhtml.write_open_tag_line('body')

        xhtml.write_tag_line('p', 'Internal error:', _class="error")
        trace = ''.join(traceback.format_exception(*sys.exc_info()))
        trace = trace.replace('<', '&lt;')
        trace = trace.replace('>', '&gt;')
        xhtml.write_tag_line('pre', trace)
        xhtml.write_close_tag_line('body')
        xhtml.write_close_tag_line('html')
        return apache.OK
