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

    def testCreateDuplicate(self):
        self.assertRaises(IntegrityError, Website.objects.create,
                          url='http://browsershots.org/')
        transaction.rollback()


class UrlTestCase(TestCase):

    def assertInvalid(self, url):
        try:
            website = Website.objects.create(url=url)
            website.delete()
            self.fail("invalid URL did not raise IntegrityError: '%s'" % url)
        except IntegrityError:
            transaction.rollback()

    def assertValid(self, url):
        self.assertEqual(Website.objects.filter(url=url).count(), 0)
        try:
            website = Website.objects.create(url=url)
            website.save()
            transaction.commit()
        except IntegrityError:
            self.fail("valid URL raised IntegrityError: '%s'" % url)
        self.assertEqual(Website.objects.filter(url=url).count(), 1)
        website.delete()
        transaction.commit()
        self.assertEqual(Website.objects.filter(url=url).count(), 0)

    def testInvalidA(self): self.assertInvalid('')
    def testInvalidB(self): self.assertInvalid(' ')
    def testInvalidC(self): self.assertInvalid('h')
    def testInvalidD(self): self.assertInvalid('http')
    def testInvalidE(self): self.assertInvalid('http:')
    def testInvalidF(self): self.assertInvalid('http:/')
    def testInvalidG(self): self.assertInvalid('http://')
    def testInvalidH(self): self.assertInvalid('http:///')
    def testInvalidI(self): self.assertInvalid('http://browsershots/')
    def testInvalidJ(self): self.assertInvalid('htp://browsershots.org/')
    def testInvalidK(self): self.assertInvalid('http//browsershots.org/')
    def testInvalidL(self): self.assertInvalid('http:/browsershots.org/')
    def testInvalidM(self): self.assertInvalid('http://browsershots.org')
    def testInvalidN(self): self.assertInvalid('http://browsershots.org/ ')
    def testInvalidO(self): self.assertInvalid(' http://browsershots.org/')

    def testValidA(self):
        self.assertValid('http://browsershots.org/')
    def testValidB(self):
        self.assertValid('http://browsershots.org/http://example.com/')
    def testValidC(self):
        self.assertValid('http://browsershots.org/robots.txt')
    def testValidD(self):
        self.assertValid('http://browsershots.org/?url=http://example.com/')
    def testValidE(self):
        self.assertValid('https://browsershots.org/')
