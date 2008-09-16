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
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import xmlrpclib
from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django import db
from django.db import IntegrityError, transaction
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.functional import update_wrapper
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.models import Factory, ScreenSize, ColorDepth
from shotserver05.factories import xmlrpc as factories
from shotserver05.xmlrpc.tests import TestServerProxy, authenticate
from shotserver05.users.tests import TESTCLIENT_PASSWORD
from shotserver05.system.utils import signature

TESTFACTORY_SECRET = ''.join("""
xEcYUVx+3H4tFABMleVTm6DFd9NW1Z7cDJWQNnMWEP19jPrj0EMi8ux8Kp1uutiv
4Xf/UOLeOvpW3A5vX/0+aZT4B+ktsT+6j/50MjceG5bQY4pmVf1cg4JKqgl4FdOY
wd4d6DReY8uCXa8WUexiIuQvGdGHqk2wsBypVlnfZTZMHzHG4ivdufRXzgTE6+Ar
VbiQLrIXsvElzbkrETcqxefvtNX23cjTXqWZo7XoL5tk5u6d2pjEn/DM6JGWXtWx
ZaraPQpTaEZx5T8NGva0DDcFJewJH4jMTer9UqQOf57Ld73+XAz7U3AEm7lsezNQ
6hmq3MxgKJVm9zCdIIxQh0EmOLQkrmajw2pLM8JMoHxBoxvaQKe6TkxRBnkSIQVF
CMT326GQKUFzowhEZipydkp4myc7XctfyZ6gBIXUXHaRBd/4hYyF0i3XJX2cDMt9
5zbQncx+k44N4c+N/VKg2c8cOezIrtXcotKQ7Bxet2/u1ZGIEc2yR45f3iwwRqQ5
""".split())


def debug(func):

    def wrapper(*args, **kwargs):
        old_setting = settings.DEBUG
        db.reset_queries()
        settings.DEBUG = True # collect database queries
        result = func(*args, **kwargs)
        settings.DEBUG = old_setting # restore old setting
        return result

    update_wrapper(wrapper, func)
    return wrapper


class FactoryTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.testfactory = Factory.objects.get(name='testfactory')

    def testAttributes(self):
        self.assertEqual(self.testfactory.get_absolute_url(),
                         '/factories/testfactory/')
        self.assertEqual(len(self.testfactory.secret_key), 512)

    def testRelated(self):
        self.assertEqual(self.testfactory.screensize_set.count(), 1)
        self.assertEqual(self.testfactory.colordepth_set.count(), 1)

    def testCreate(self):
        self.factory2 = Factory.objects.create(
            name='factory2',
            user=User.objects.get(username='testclient'),
            operating_system=OperatingSystem.objects.get(slug='leopard'))


class ScreenSizeTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.testfactory = Factory.objects.get(name='testfactory')

    def testDuplicate(self):
        existing = self.testfactory.screensize_set.all()[0]
        self.assertRaises(IntegrityError,
            ScreenSize.objects.create, factory=self.testfactory,
            width=existing.width, height=existing.height)
        transaction.rollback()

    def testValidate(self):
        self.assert_(ScreenSize.validate(240, 320))
        self.assert_(ScreenSize.validate(320, 240))
        self.assert_(ScreenSize.validate(640, 480))
        self.assert_(ScreenSize.validate(800, 600))
        self.assert_(ScreenSize.validate(1024, 768))
        self.assert_(ScreenSize.validate(1280, 1024))
        self.assert_(ScreenSize.validate(1680, 1050))
        self.assertRaises(ValidationError, ScreenSize.validate, 239, 480)
        self.assertRaises(ValidationError, ScreenSize.validate, 1681, 1050)


class ColorDepthTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.testfactory = Factory.objects.get(name='testfactory')

    def testDuplicate(self):
        existing = self.testfactory.colordepth_set.all()[0]
        self.assertRaises(IntegrityError,
            ColorDepth.objects.create, factory=self.testfactory,
            bits_per_pixel=existing.bits_per_pixel)
        transaction.rollback()

    def testValidate(self):
        self.assert_(ColorDepth.validate(1))
        self.assert_(ColorDepth.validate(4))
        self.assert_(ColorDepth.validate(8))
        self.assert_(ColorDepth.validate(15))
        self.assert_(ColorDepth.validate(16))
        self.assert_(ColorDepth.validate(24))
        self.assert_(ColorDepth.validate(32))
        self.assertRaises(ValidationError, ColorDepth.validate, 33)
        self.assertRaises(ValidationError, ColorDepth.validate, 0)
        self.assertRaises(ValidationError, ColorDepth.validate, -1)
        self.assertRaises(ValidationError, ColorDepth.validate, -24)


class XMLRPCTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.server = TestServerProxy(self.client)
        self.testfactory = Factory.objects.get(name='testfactory')

    def testAuth(self):
        self.assertEqual(
            signature('factories.testAuth'),
            ['string', 'string', 'int', 'string', 'string', 'string'])
        args = ['testfactory', 123, 'hello']
        authenticate('factories.testAuth', args, TESTFACTORY_SECRET)
        self.assertEquals(self.server.factories.testAuth(*args), 'OK')

    def testCreateFactory(self):
        self.assertEqual(signature('factories.createFactory'), 7 * ['string'])
        args = ['testclient', 'smug', 'leopard', 'MacBook']
        authenticate('factories.createFactory', args, TESTCLIENT_PASSWORD)
        response = self.server.factories.createFactory(*args)
        self.assertEqual(response, 'OK')

    @debug
    def testUpdateFactory(self):
        self.assertEqual(signature('factories.updateFactory'), ['string'] * 7)
        args = ['testclient', 'testfactory', 'panther', 'iBook G4']
        authenticate('factories.updateFactory', args, TESTCLIENT_PASSWORD)
        self.assertEqual(self.server.factories.updateFactory(*args), 'OK')
        sql = db.connection.queries[-1]['sql']
        self.assert_(sql.startswith('UPDATE "factories_factory"'))
        self.assert_('"hardware" = iBook G4' in sql)
        self.assert_('"operating_system_id" = 4' in sql)
        self.assert_('"name" = ' not in sql)
        self.assert_('"last_upload" = ' not in sql)

    def testListActiveFactories(self):
        self.assertEqual(signature('factories.listActiveFactories'), ['list'])
        active = self.server.factories.listActiveFactories()
        self.assertEqual(len(active), 0)

    def testFactoryDetails(self):
        self.assertEqual(signature('factories.factoryDetails'),
                         ['dict', 'string'])
        details = self.server.factories.factoryDetails('testfactory')
        self.assertEqual(details['name'], 'testfactory')
        self.assertEqual(details['operating_system'], 'leopard')
        self.assertEqual(details['hardware'], 'MacBook')
        self.assertEqual(details['last_poll'], '')
        self.assertEqual(details['last_upload'], '')
        self.assertEqual(details['last_error'], '')

    def testAddScreenSize(self):
        self.assertEqual(signature('factories.addScreenSize'),
            ['string', 'string', 'string', 'int', 'int', 'string', 'string'])
        args = ['testclient', 'testfactory', 1024, 768]
        authenticate('factories.addScreenSize', args, TESTCLIENT_PASSWORD)
        self.assertEqual(self.testfactory.screensize_set.count(), 1)
        self.assertEqual(self.server.factories.addScreenSize(*args), 'OK')
        self.assertEqual(self.testfactory.screensize_set.count(), 2)
        # Adding the same screen size again should fail.
        self.assertRaises(xmlrpclib.Fault,
                          self.server.factories.addScreenSize, *args)
        transaction.rollback()
        self.assertEqual(self.testfactory.screensize_set.count(), 2)

    def testAddColorDepth(self):
        self.assertEqual(signature('factories.addColorDepth'),
            ['string', 'string', 'string', 'int', 'string', 'string'])
        args = ['testclient', 'testfactory', 16]
        authenticate('factories.addColorDepth', args, TESTCLIENT_PASSWORD)
        self.assertEqual(self.testfactory.colordepth_set.count(), 1)
        self.assertEqual(self.server.factories.addColorDepth(*args), 'OK')
        self.assertEqual(self.testfactory.colordepth_set.count(), 2)
        # Adding the same color depth again should fail.
        self.assertRaises(xmlrpclib.Fault,
                          self.server.factories.addColorDepth, *args)
        transaction.rollback()
        self.assertEqual(self.testfactory.colordepth_set.count(), 2)
