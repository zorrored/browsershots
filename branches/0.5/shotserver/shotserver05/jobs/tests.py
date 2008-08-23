from django.test import TestCase
from django.db import transaction
from shotserver05.jobs.models import Group, Job


class PlatformTestCase(TestCase):

    def setUp(self):
        transaction.rollback()
        self.group = Group.objects.create()
        self.job1 = Job.objects.create(group=self.group)
        self.job2 = Job.objects.create(group=self.group)
