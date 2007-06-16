# browsershots.org - Test your web design in different browsers
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
Test suite for browsers app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from psycopg import IntegrityError, ProgrammingError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture
from shotserver04.platforms.models import Platform, OperatingSystem
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Engine, BrowserGroup, Browser


class SizeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.factory = Factory.objects.create(
            name='factory',
            admin=self.user,
            architecture=Architecture.objects.get(pk=1),
            operating_system=OperatingSystem.objects.get(pk=1))
        self.engine = Engine.objects.get(pk=1)
        self.browser_group = BrowserGroup.objects.get(pk=1)

    def tearDown(self):
        self.factory.delete()
        self.user.delete()

    def createBrowser(self, user_agent, **kwargs):
        return Browser.objects.create(
            factory=self.factory,
            user_agent=user_agent,
            browser_group=self.browser_group,
            version=kwargs.get('version', ''),
            major=kwargs.get('major', 0),
            minor=kwargs.get('minor', 0),
            engine=self.engine,
            engine_version=kwargs.get('engine_version', ''),
            javascript_id=kwargs.get('javascript', 1),
            java_id=kwargs.get('java', 1),
            flash_id=kwargs.get('flash', 1),
            command=kwargs.get('command', ''),
            active=kwargs.get('active', True),
            )

    def assertBrowserValid(self, user_agent, **kwargs):
        try:
            self.createBrowser(user_agent, **kwargs).delete()
        except (IntegrityError, ProgrammingError):
            transaction.rollback()
            self.fail('\n'.join((
                "could not create browser with valid settings:",
                '"%s"' % user_agent, repr(kwargs))))

    def assertBrowserInvalid(self, user_agent, **kwargs):
        try:
            try:
                self.createBrowser(user_agent, **kwargs).delete()
                self.fail('\n'.join((
                    "created browser with invalid settings:",
                    '"%s"' % user_agent, repr(kwargs))))
            except IntegrityError:
                pass
        finally:
            transaction.rollback()

    def testFirefox15(self):
        self.assertBrowserValid('Firefox/1.5.0.8',
                                version='1.5.0.8', major=1, minor=5)

    def testFirefox20(self):
        self.assertBrowserValid('Firefox/2.0.0.1',
                                version='2.0.0.1', major=2, minor=0)

    def testGecko(self):
        self.assertBrowserValid('Gecko/20061226 Firefox/2.0.0.1',
                                version='2.0.0.1', major=2, minor=0,
                                engine_version='20061226')

    def testBogusVersion(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.2', major=2, minor=0)

    def testBogusMajor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=1, minor=0)

    def testBogusMinor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=2, minor=1)

    def testBogusMajorMinor(self):
        self.assertBrowserInvalid('Firefox/2.0.0.1',
                                  version='2.0.0.1', major=0, minor=1)

    def testBogusEngine(self):
        self.assertBrowserInvalid('Gecko/20061226 Firefox/2.0.0.1',
                                  version='2.0.0.1', major=2, minor=0,
                                  engine_version='20061220')
