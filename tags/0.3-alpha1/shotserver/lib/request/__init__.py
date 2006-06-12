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
Additional info about a mod_python Apache request object.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

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
