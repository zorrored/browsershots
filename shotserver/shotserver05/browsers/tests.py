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
Tests for browsers app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from shotserver05.factories.models import Factory
from shotserver05.platforms.models import Platform, OperatingSystem
from shotserver05.browsers.models import BrowserName, Engine, Browser


class BrowserNameTestCase(TestCase):

    def setUp(self):
        self.firefox = BrowserName.objects.get(name='Firefox')

    def testAttributes(self):
        self.assertEqual(self.firefox.name, 'Firefox')

    def testDuplicate(self):
        self.assertRaises(IntegrityError,
                          BrowserName.objects.create, name='Firefox')
        transaction.rollback()


class EngineTestCase(TestCase):

    def setUp(self):
        self.gecko = Engine.objects.get(name='Gecko')

    def testAttributes(self):
        self.assertEqual(self.gecko.name, 'Gecko')

    def testDuplicate(self):
        self.assertRaises(IntegrityError,
                          Engine.objects.create, name='Gecko')
        transaction.rollback()


class BrowserTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories', 'test_browsers']

    def setUp(self):
        self.firefox30 = Browser.objects.get(
            factory=Factory.objects.get(name='testfactory'),
            name=BrowserName.objects.get(name='Firefox'),
            major=3, minor=0)

    def testVersion(self):
        self.assertEqual(self.firefox30.version, '3.0.1')
        self.assertEqual(self.firefox30.major, 3)
        self.assertEqual(self.firefox30.minor, 0)
        self.assertEqual(self.firefox30.get_short_version(), '3.0')

    def testDuplicate(self):
        self.assertRaises(IntegrityError,
                          Browser.objects.create,
                          factory=self.firefox30.factory,
                          name=self.firefox30.name,
                          version='3.0.1',
                          major=3, minor=0,
                          engine=self.firefox30.engine,
                          engine_version=self.firefox30.engine_version,
                          user_agent=self.firefox30.user_agent)
        transaction.rollback()
