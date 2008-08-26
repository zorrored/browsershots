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
        self.assert_('xp' in os_list)
        self.assert_('hardy' in os_list)

    def testOperatingSystemDetails(self):
        self.assertEqual(signature('platforms.operatingSystemDetails'),
                         ['dict', 'string'])
        details = self.server.platforms.operatingSystemDetails('leopard')
        self.assertEqual(details['platform'], 'Mac')
        self.assertEqual(details['name'], 'Mac OS X')
        self.assertEqual(details['version'], '10.5')
        self.assertEqual(details['codename'], 'Leopard')
