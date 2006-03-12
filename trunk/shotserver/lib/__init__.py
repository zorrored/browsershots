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

from mod_python import apache
from interface import xhtml

def write_html_head():
    req.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"')
    req.write(' "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    xhtml.write_open_tag_line('html', xmlns="http://www.w3.org/1999/xhtml")

def handler(req):
    """
    Process all incoming HTTP requests.
    """
    try:
        __builtins__['req'] = req
        req.info = request.RequestInfo()

        req.status = apache.OK
        req.content_type = 'application/xhtml+xml; charset=UTF-8'

    except:
        if naked == 'redirect':
            write_html_head()

        while len(xhtml.open_tags) > 2:
            xhtml.write_close_tag_line()
        if xhtml.open_tags[-1] == 'head':
            xhtml.write_close_tag_line('head')
        if xhtml.open_tags[-1] != 'body':
            xhtml.write_open_tag_line('body')
        # xhtml.write_tag_line('br')
        xhtml.write_tag_line('p', 'Internal error:', _class="error")
        trace = ''.join(traceback.format_exception(*sys.exc_info()))
        trace = trace.replace('<', '&lt;')
        trace = trace.replace('>', '&gt;')
        xhtml.write_tag_line('pre', trace)
        xhtml.write_close_tag_line('body')
        xhtml.write_close_tag_line('html')
        return apache.OK
