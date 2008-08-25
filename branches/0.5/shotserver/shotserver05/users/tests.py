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
            signature('users.testAuth'),
            ['string', 'string', 'int', 'string', 'string', 'string'])
        args = ['testclient', 123, 'hello']
        authenticate('users.testAuth', args, TESTCLIENT_PASSWORD)
        self.assertEquals(self.server.users.testAuth(*args), 'OK')
