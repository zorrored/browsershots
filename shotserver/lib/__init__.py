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
Top-level shotserver module.
All HTTP requests are handled from here.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import sys, traceback
from mod_python import apache
from shotserver03 import request
from shotserver03.interface import xhtml
from shotserver03.segments import metamenu, topmenu, bottom

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

def action_option(module, key, default):
    if hasattr(module, key):
        return module.__dict__[key]()
    else:
        return default

def negotiate_xml():
    if not req.headers_in.has_key('Accept'):
        return True # Send XML to validator.w3.org etc.
    if req.headers_in['Accept'].count('application/xhtml+xml'):
        return True # Send XML to all modern browsers.
    return False # Send text/html to MSIE 6 and 7.

def write_html_head(title):
    req.content_type = 'text/html; charset=UTF-8'
    xml = negotiate_xml()
    if xml:
        req.content_type = 'application/xhtml+xml; charset=UTF-8'
    req.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"')
    req.write(' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    xhtml.write_open_tag_line('html', xmlns="http://www.w3.org/1999/xhtml")
    xhtml.write_open_tag_line('head')
    if xml:
        xhtml.write_tag_line('title', '%s - Browsershots' % title)
    else:
        xhtml.write_tag_line('title', 'This browser does not understand XML')
    xhtml.write_tag_line('link', type="text/css", href="/style/style.css", rel="stylesheet")
    xhtml.write_tag_line('script', '', type="text/javascript", src="/style/zoom.js")
    xhtml.write_tag_line('script', '', type="text/javascript", src="/style/forms.js")
    xhtml.write_close_tag_line('head')

def handler(req):
    """
    Process all incoming HTTP requests.
    """
    try:
        __builtins__['req'] = req
        req.info = request.RequestInfo()

        if req.method == 'POST':
            action_module = import_deep('shotserver03.post.%s' % req.info.action)
            assert action_module.redirect()
            req.status = apache.HTTP_MOVED_TEMPORARILY
            return apache.HTTP_MOVED_TEMPORARILY

        assert req.method == 'GET' or req.method == 'HEAD'
        action_module = import_deep('shotserver03.get.%s' % req.info.action)
        if hasattr(action_module, 'redirect'):
            if action_module.redirect():
                req.status = apache.HTTP_MOVED_TEMPORARILY
                return apache.HTTP_MOVED_TEMPORARILY

        title = action_option(action_module, 'title', 'Browsershots')
        write_html_head(title)

        xhtml.write_open_tag_line('body')
        xhtml.write_open_tag_line('div', _id="main")

        metamenu.write()
        topmenu.write()

        xhtml.write_open_tag_line('div', _class="menu", _id="headline")
        xhtml.write_tag_line('img', src="/style/logo40.png", _class="right", alt="browsershots.org beta")
        xhtml.write_tag_line('h1', title)
        xhtml.write_close_tag_line('div') # id="sub"

        action_module.body()

        # req.info.write_table()
        bottom.write()

        xhtml.write_close_tag_line('div') # id="all"
        xhtml.write_close_tag_line('body')
        xhtml.write_close_tag_line('html')
        return apache.OK
    except apache.SERVER_RETURN:
        raise
    except:
        while len(xhtml.open_tags) > 2:
            xhtml.write_close_tag_line()
        if xhtml.open_tags and xhtml.open_tags[-1] == 'head':
            xhtml.write_close_tag_line('head')
        if xhtml.open_tags and xhtml.open_tags[-1] != 'body':
            xhtml.write_open_tag_line('body')

        xhtml.write_open_tag_line('div', _class="traceback")
        xhtml.write_tag_line('p', 'Internal error:', _class="error")
        trace = ''.join(traceback.format_exception(*sys.exc_info()))
        trace = trace.replace('<', '&lt;')
        trace = trace.replace('>', '&gt;')
        xhtml.write_tag_line('pre', trace)
        xhtml.write_tag_line('p', 'If this problem persists, please <a href="mailto:johann@browsershots.org">send a bug report</a>.')
        xhtml.write_close_tag_line('div') # class="traceback"
        if len(xhtml.open_tags) == 2:
            xhtml.write_close_tag_line('body')
            xhtml.write_close_tag_line('html')
        return apache.OK
