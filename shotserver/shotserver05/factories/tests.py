from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.models import Factory
from shotserver05.factories import xmlrpc as factories
from shotserver05.xmlrpc.tests import \
    TestServerProxy, authenticate, TESTCLIENT_PASSWORD, FACTORY1_SECRET


class FactoryTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.factory1 = Factory.objects.get(name='factory1')

    def testAttributes(self):
        self.assertEqual(self.factory1.get_absolute_url(),
                         '/factories/factory1/')
        self.assertEqual(len(self.factory1.secret_key), 512)

    def testRelated(self):
        self.assertEqual(self.factory1.screensize_set.count(), 1)
        self.assertEqual(self.factory1.colordepth_set.count(), 1)

    def testCreate(self):
        self.factory2 = Factory.objects.create(
            name='factory2',
            user=User.objects.get(username='testclient'),
            operating_system=OperatingSystem.objects.get(slug='leopard'))


class XMLRPCTestCase(TestCase):
    fixtures = ['authtestdata', 'test_factories']

    def setUp(self):
        self.server = TestServerProxy(self.client)

    def testCreateFactory(self):
        args = ['testclient', 'smug', 'leopard', 'MacBook']
        authenticate('factories.createFactory', args, TESTCLIENT_PASSWORD)
        response = self.server.factories.createFactory(*args)
        self.assertEqual(response, 'OK')

    def testDetails(self):
        details = self.server.factories.details('factory1')
        self.assertEqual(details['name'], 'factory1')
        self.assertEqual(details['operating_system'], 'leopard')
        self.assertEqual(details['hardware'], 'MacBook')
        self.assertEqual(details['last_poll'], '')
        self.assertEqual(details['last_upload'], '')
        self.assertEqual(details['last_error'], '')
