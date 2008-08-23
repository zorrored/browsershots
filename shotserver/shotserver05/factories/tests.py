from django.test import TestCase
from django.contrib.auth.models import User
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.models import Factory


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
