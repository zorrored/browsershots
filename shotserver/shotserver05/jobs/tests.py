from django.test import TestCase
from django.db import transaction
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import BrowserName
from shotserver05.jobs.models import JobGroup, Job


class JobTestCase(TestCase):
    fixtures = ['test_browsers', 'test_websites']

    def setUp(self):
        transaction.rollback()
        self.job_group = JobGroup.objects.create(website_id=1)
        self.mac = Platform.objects.get(name='Mac')
        self.firefox = BrowserName.objects.get(name='Firefox')
        self.safari = BrowserName.objects.get(name='Safari')
        self.firefox20 = Job.objects.create(
            group=self.job_group, platform=self.mac,
            browser_name=self.firefox, major=2, minor=0)
        self.firefox30 = Job.objects.create(
            group=self.job_group, platform=self.mac,
            browser_name=self.firefox, major=3, minor=0)
        self.safari = Job.objects.create(
            group=self.job_group, platform=self.mac,
            browser_name=self.safari, major=3, minor=1)

    def testJob(self):
        self.assertEqual(self.firefox20.browser_name.name, 'Firefox')
        self.assertEqual(self.firefox20.major, 2)
        self.assertEqual(self.firefox20.minor, 0)
        self.assertEqual(self.firefox20.browser_name,
                         self.firefox30.browser_name)
        self.assertEqual(self.safari.browser_name.name, 'Safari')
        self.assertEqual(self.safari.major, 3)
        self.assertEqual(self.safari.minor, 1)
