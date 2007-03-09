from psycopg import IntegrityError
from unittest import TestCase
from django.db import transaction
from shotserver04.websites.models import Website


class WebsitesTestCase(TestCase):

    def setUp(self):
        self.website = Website.objects.create(url='http://browsershots.org/')
        self.website.save()
        transaction.commit()

    def tearDown(self):
        self.website.delete()
        transaction.commit()

    def testChangeURL(self):
        self.website.url = 'https://browsershots.org/websites/'
        self.website.save()
        transaction.commit()
        self.assertEqual(len(Website.objects.filter(
            url__contains='browsershots.org')), 1)

    def testEmptyURL(self):
        self.website.url = ''
        self.assertRaises(IntegrityError, self.website.save)
        transaction.rollback()

    def testInvalidURL(self):
        self.website.url = '-'
        self.assertRaises(IntegrityError, self.website.save)
        transaction.rollback()

    def testCreateDuplicate(self):
        self.assertRaises(IntegrityError, Website.objects.create,
                          url='http://browsershots.org/')
        transaction.rollback()

    def testCreateEmpty(self):
        self.assertRaises(IntegrityError, Website.objects.create, url='')
        transaction.rollback()

    def testCreateInvalid(self):
        self.assertRaises(IntegrityError, Website.objects.create, url='-')
        transaction.rollback()
