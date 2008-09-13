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
Tests for the platforms app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.test import TestCase
from django.db import transaction
from shotserver05.system.utils import signature
from shotserver05.xmlrpc.tests import TestServerProxy
from shotserver05.platforms.models import Platform, OperatingSystem


class PlatformTestCase(TestCase):

    def setUp(self):
        transaction.rollback()

    def testSlug(self):
        for platform in Platform.objects.all():
            self.assertEqual(platform.name.lower(), platform.slug)


class XMLRPCTestCase(TestCase):

    def setUp(self):
        transaction.rollback()
        self.server = TestServerProxy(self.client)

    def testListOperatingSystems(self):
        self.assertEqual(signature('platforms.listOperatingSystems'),
                         ['list'])
        os_list = self.server.platforms.listOperatingSystems()
        self.assert_('leopard' in os_list)
        self.assert_('winxp' in os_list)
        self.assert_('hardy' in os_list)

    def testOperatingSystemDetails(self):
        self.assertEqual(signature('platforms.operatingSystemDetails'),
                         ['dict', 'string'])
        details = self.server.platforms.operatingSystemDetails('leopard')
        self.assertEqual(details['platform'], 'Mac')
        self.assertEqual(details['name'], 'Mac OS X')
        self.assertEqual(details['version'], '10.5')
        self.assertEqual(details['codename'], 'Leopard')
