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
        self.assert_('users.testAuth' in methods)

    def testMethodSignature(self):
        self.assertEqual(
            self.server.system.methodSignature('system.methodSignature'),
            [['list', 'string']])

    def testMethodHelp(self):
        self.assertEqual(signature('system.methodHelp'), 2 * ['string'])
        help = self.server.system.methodHelp('system.methodHelp')
        self.assert_('\nArguments:\n' in help)
        self.assert_('\nReturn value:\n' in help)
