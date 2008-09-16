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
Tests for the systems app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.test import TestCase
from shotserver05.xmlrpc.tests import TestServerProxy
from shotserver05.system.utils import signature


class XMLRPCTestCase(TestCase):

    def setUp(self):
        self.server = TestServerProxy(self.client)

    def testListMethods(self):
        self.assertEqual(signature('system.listMethods'), ['list'])
        methods = self.server.system.listMethods()
        self.assert_('system.listMethods' in methods)
        self.assert_('factories.createFactory' in methods)
        self.assert_('accounts.testAuth' in methods)

    def testMethodSignature(self):
        self.assertEqual(
            self.server.system.methodSignature('system.methodSignature'),
            [['list', 'string']])

    def testMethodHelp(self):
        self.assertEqual(signature('system.methodHelp'), 2 * ['string'])
        help = self.server.system.methodHelp('system.methodHelp')
        self.assert_('\nArguments:\n' in help)
        self.assert_('\nReturn value:\n' in help)
