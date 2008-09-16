# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Tests for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.test import TestCase
from shotserver05.xmlrpc.tests import TestServerProxy, authenticate
from shotserver05.system.utils import signature

TESTCLIENT_PASSWORD = 'sha1$6efc0$f93efe9fd7542f25a7be94871ea45aa95de57161'


class XMLRPCTestCase(TestCase):
    fixtures = ['authtestdata']

    def setUp(self):
        self.server = TestServerProxy(self.client)

    def testAuth(self):
        self.assertEqual(
            signature('accounts.testAuth'),
            ['string', 'string', 'int', 'string', 'string', 'string'])
        args = ['testclient', 123, 'hello']
        authenticate('accounts.testAuth', args, TESTCLIENT_PASSWORD)
        self.assertEquals(self.server.accounts.testAuth(*args), 'OK')
