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
Insert a new website into the database.
"""

__revision__ = '$Rev: 117 $'
__date__ = '$Date: 2006-04-08 08:51:18 +0200 (Sat, 08 Apr 2006) $'
__author__ = '$Author: johann $'

from shotserver03.interface import xhtml
from shotserver03 import database

def read_form(form):
    url = ''
    for key in form.keys():
        if key == 'url':
            url = form[key]
        elif key == 'submit':
            pass
        else:
            raise "unexpected input: %s" % key
    return url

def select_or_insert(url):
    """
    Get the website id of a URL. Insert URL into website table if necessary.
    """
    database.connect()
    try:
        cur.execute("SELECT website FROM website WHERE url=%s", url)
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO website (url) VALUES (%s)", url)
            cur.execute("SELECT website FROM website WHERE url=%s", url)
            row = cur.fetchone()
        return row['website']
    finally:
        database.disconnect()

def redirect():
    url = read_form(req.info.form)
    website = select_or_insert(url)
    req.headers_out['Location'] = '/website/%d/' % website
    return True
