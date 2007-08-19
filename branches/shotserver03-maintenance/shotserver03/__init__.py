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
Top-level shotserver module.
All HTTP requests are handled from here.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import traceback
from shotserver03 import request, xmlrpc, database
from shotserver03.interface import xhtml, human
from shotserver03.segments import languages, logo, topmenu, bottom

DEBUG_XML_IN_TITLE = False


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
    """
    Get an option from a function in an action module.
    If the function does not exist, return the default value.
    """
    if hasattr(module, key):
        return module.__dict__[key]()
    else:
        return default


def negotiate_xml():
    """
    Check if the client can handle application/xhtml+xml.
    """
    if not 'Accept' in req.headers_in:
        return True # Send XML to validator.w3.org etc.
    if req.headers_in['Accept'].count('application/xhtml+xml'):
        return True # Send XML to all modern browsers.
    return False # Send text/html to MSIE 6 and 7.


def write_html_head(title):
    """
    Send HTTP header and XHTML head.
    """
    req.content_type = 'text/html; charset=UTF-8'
    xml = negotiate_xml()
    if xml:
        req.content_type = 'application/xhtml+xml; charset=UTF-8'
    req.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"')
    req.write(' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    xhtml.write_open_tag_line('html', xmlns="http://www.w3.org/1999/xhtml")
    xhtml.write_open_tag_line('head')
    if DEBUG_XML_IN_TITLE and not xml:
        xhtml.write_tag_line('title', 'This browser does not understand XML')
    else:
        xhtml.write_tag_line('title', '%s - Browsershots' % title)
    xhtml.write_tag_line('link', type="text/css", rel="stylesheet",
                         href="/style/style.css")
    xhtml.write_tag_line('script', '', type="text/javascript",
                         src="/style/zoom.js")
    xhtml.write_tag_line('script', '', type="text/javascript",
                         src="/style/forms.js")
    xhtml.write_tag_line('meta', _name="verify-v1",
        content="gqd9KWCCzoBsvkG2YjB2wkPzq57FwLCH/jZF8hinW24=")
    xhtml.write_close_tag_line('head')


def google_analytics(https=False):
    """
    Load and run urchin.js for Google Analytics.
    """
    if https:
        req.write('<script src="https://ssl.google-analytics.com/urchin.js" ')
    else:
        req.write('<script src="http://www.google-analytics.com/urchin.js" ')
    req.write("""\
type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-939486-1";
urchinTracker();
</script>
""")


def handler(req):
    """
    Process a HTTP request.
    """
    if req.uri.strip('/') == 'shotserver/RPC2':
        return xmlrpc.handler(req)

    from mod_python import apache
    try:
        __builtins__['req'] = req
        req.info = request.RequestInfo()
        req.params = request.params.Params()

        if req.method == 'POST':
            action_module = import_deep('shotserver03.post.%s' %
                                        req.info.action)
            assert action_module.redirect()
            req.status = apache.HTTP_MOVED_TEMPORARILY
            return apache.HTTP_MOVED_TEMPORARILY

        assert req.method == 'GET' or req.method == 'HEAD'
        action_module = import_deep('shotserver03.get.%s' % req.info.action)

        if hasattr(action_module, 'read_params'):
            action_module.read_params()

        if hasattr(action_module, 'redirect'):
            action_module.redirect()

        title = action_option(action_module, 'title', 'Browsershots')
        write_html_head(title)

        xhtml.write_open_tag_line('body')
        xhtml.write_open_tag_line('div', _id="main")

        languages.write()
        logo.write()
        topmenu.write()
        xhtml.write_tag_line('h1', title)

        action_module.body()

        # human.write_table(req.info)
        # human.write_table(req.params)

        bottom.write()

        xhtml.write_close_tag_line('div') # id="all"
        google_analytics(req.info.uri.protocol == 'https')

        xhtml.write_close_tag_line('body')
        xhtml.write_close_tag_line('html')
        database.disconnect()
        return apache.OK
    except apache.SERVER_RETURN:
        database.disconnect()
        raise
    except ImportError:
        return apache.HTTP_NOT_FOUND # 404
    except:
        database.disconnect()
        while xhtml.open_tags and xhtml.open_tags[-1] != 'body':
            xhtml.write_close_tag_line()
        if xhtml.open_tags and xhtml.open_tags[-1] == 'head':
            xhtml.write_close_tag_line('head')
        if xhtml.open_tags and xhtml.open_tags[-1] != 'body':
            xhtml.write_open_tag_line('body')

        xhtml.write_open_tag_line('div', _class="traceback")
        xhtml.write_tag_line('p', 'Internal error:', _class="error")
        trace = ''.join(traceback.format_exc())
        trace = trace.replace('<', '&lt;')
        trace = trace.replace('>', '&gt;')
        xhtml.write_tag_line('pre', trace)
        message = "If this problem persists, please <a>send a bug report</a>."
        message.replace('<a>', '<a href="mailto:johann@browsershots.org">')
        xhtml.write_tag_line('p', message)
        xhtml.write_close_tag_line('div') # class="traceback"
        if len(xhtml.open_tags) == 2:
            xhtml.write_close_tag_line('body')
            xhtml.write_close_tag_line('html')
        raise
