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
Additional info about a mod_python Apache request object.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.request import uri, params
from shotserver03.interface import xhtml


class RequestInfo:
    """
    Additional info about a mod_python Apache request object.
    """

    def __init__(self, basepath = ''):
        from mod_python import util
        self.form = util.FieldStorage(req)
        self.uri = uri.URI(basepath)

        self.options = self.uri.parts
        if len(self.options) and self.options[-1] == '':
            self.options.pop()

        if len(self.options) and self.options[0] == 'intl':
            self.lang = self.options[1]
            self.options = self.options[2:]

        if len(self.options):
            self.action = self.options[0]
            self.options = self.options[1:]
        else:
            self.action = 'start'
