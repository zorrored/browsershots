from django.test import TestCase
from django.db import transaction
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import BrowserName
from shotserver05.jobs.models import Group, Job


class JobTestCase(TestCase):
    fixtures = ['test_browsers', 'test_websites']

    def setUp(self):
        transaction.rollback()
        self.group = Group.objects.create(
            website_id=1)
        self.firefox20 = Job.objects.create(
            group=self.group,
            platform=Platform.objects.get(name='Mac'),
            browser_name=BrowserName.objects.get(name='Firefox'),
            major=2, minor=0)
        self.firefox30 = Job.objects.create(
            group=self.group,
            platform=Platform.objects.get(name='Mac'),
            browser_name=BrowserName.objects.get(name='Firefox'),
            major=3, minor=0)
        self.safari = Job.objects.create(
            group=self.group,
            platform=Platform.objects.get(name='Mac'),
            browser_name=BrowserName.objects.get(name='Safari'),
            major=3, minor=1)

    def testJob(self):
        self.assertEqual(self.firefox20.browser_name.name, 'Firefox')
        self.assertEqual(self.firefox20.major, 2)
        self.assertEqual(self.firefox20.minor, 0)
        self.assertEqual(self.firefox20.browser_name,
                         self.firefox30.browser_name)
        self.assertEqual(self.safari.browser_name.name, 'Safari')
        self.assertEqual(self.safari.major, 3)
        self.assertEqual(self.safari.minor, 1)
