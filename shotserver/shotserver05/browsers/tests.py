from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from shotserver05.factories.models import Factory
from shotserver05.platforms.models import Platform, OperatingSystem
from shotserver05.browsers.models import BrowserName, Engine, Browser


class BrowserNameTestCase(TestCase):

    def setUp(self):
        transaction.rollback()
        self.firefox = BrowserName.objects.get(name='Firefox')

    def testAttributes(self):
        self.assertEqual(self.firefox.name, 'Firefox')

    def testDuplicate(self):
        self.assertRaises(IntegrityError,
                          BrowserName.objects.create, name='Firefox')
        transaction.rollback()


class EngineTestCase(TestCase):

    def setUp(self):
        transaction.rollback()
        self.gecko = Engine.objects.get(name='Gecko')

    def testAttributes(self):
        self.assertEqual(self.gecko.name, 'Gecko')

    def testDuplicate(self):
        self.assertRaises(IntegrityError,
                          Engine.objects.create, name='Gecko')
        transaction.rollback()


class BrowserTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories', 'test_versions']

    def setUp(self):
        transaction.rollback()
        self.firefox30 = Browser.objects.get(
            factory=Factory.objects.get(name='factory1'),
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
