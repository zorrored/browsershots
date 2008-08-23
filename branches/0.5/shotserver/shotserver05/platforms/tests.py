from django.test import TestCase
from django.db import transaction
from shotserver05.platforms.models import Platform, OperatingSystem


class PlatformTestCase(TestCase):

    def setUp(self):
        transaction.rollback()

    def testSlug(self):
        for platform in Platform.objects.all():
            self.assertEqual(platform.name.lower(), platform.slug)
