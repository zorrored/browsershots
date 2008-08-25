from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.models import Factory
from shotserver05.factories import xmlrpc as factories
from shotserver05.xmlrpc.tests import TestServerProxy, authenticate
from shotserver05.users.tests import TESTCLIENT_PASSWORD
from shotserver05.system.utils import signature

FACTORY1_SECRET = ''.join("""
xEcYUVx+3H4tFABMleVTm6DFd9NW1Z7cDJWQNnMWEP19jPrj0EMi8ux8Kp1uutiv
4Xf/UOLeOvpW3A5vX/0+aZT4B+ktsT+6j/50MjceG5bQY4pmVf1cg4JKqgl4FdOY
wd4d6DReY8uCXa8WUexiIuQvGdGHqk2wsBypVlnfZTZMHzHG4ivdufRXzgTE6+Ar
VbiQLrIXsvElzbkrETcqxefvtNX23cjTXqWZo7XoL5tk5u6d2pjEn/DM6JGWXtWx
ZaraPQpTaEZx5T8NGva0DDcFJewJH4jMTer9UqQOf57Ld73+XAz7U3AEm7lsezNQ
6hmq3MxgKJVm9zCdIIxQh0EmOLQkrmajw2pLM8JMoHxBoxvaQKe6TkxRBnkSIQVF
CMT326GQKUFzowhEZipydkp4myc7XctfyZ6gBIXUXHaRBd/4hYyF0i3XJX2cDMt9
5zbQncx+k44N4c+N/VKg2c8cOezIrtXcotKQ7Bxet2/u1ZGIEc2yR45f3iwwRqQ5
""".split())


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

    def testAuth(self):
        self.assertEqual(
            signature('factories.testAuth'),
            ['string', 'string', 'int', 'string', 'string', 'string'])
        args = ['factory1', 123, 'hello']
        authenticate('factories.testAuth', args, FACTORY1_SECRET)
        self.assertEquals(self.server.factories.testAuth(*args), 'OK')

    def testCreateFactory(self):
        self.assertEqual(signature('factories.createFactory'), 7 * ['string'])
        args = ['testclient', 'smug', 'leopard', 'MacBook']
        authenticate('factories.createFactory', args, TESTCLIENT_PASSWORD)
        response = self.server.factories.createFactory(*args)
        self.assertEqual(response, 'OK')

    def testDetails(self):
        self.assertEqual(signature('factories.details'), ['dict', 'string'])
        details = self.server.factories.details('factory1')
        self.assertEqual(details['name'], 'factory1')
        self.assertEqual(details['operating_system'], 'leopard')
        self.assertEqual(details['hardware'], 'MacBook')
        self.assertEqual(details['last_poll'], '')
        self.assertEqual(details['last_upload'], '')
        self.assertEqual(details['last_error'], '')
