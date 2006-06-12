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
URI information about a HTTP request.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

class IncorrectBasepathError(Exception):
    """The given base path does not match the actual URI."""
    pass

class URI:
    """
    Make request URI more explicit.
    """

    def __init__(self, basepath = ''):
        self.hostname = req.hostname
        self.raw = req.uri

        while basepath.endswith('/'):
            basepath = basepath[:-1]
        self.basepath = basepath
        fullbase = basepath + '/shotserver'

        self.parts = self.raw.split('/')
        for basepart in fullbase.split('/'):
            if basepart != self.parts[0]:
                raise IncorrectBasepathError('%s != %s' %
                    (repr(basepart), repr(self.parts[0])))
            self.parts.pop(0)

        self.lang = '' # self.parts.pop()
