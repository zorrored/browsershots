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
            transaction.commit()
        except IntegrityError:
            transaction.rollback()
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
    def testInvalidM(self): self.assertInvalid('http://browsershots.org:abc/')
    def testInvalidN(self): self.assertInvalid('http://browsershots.org')
    def testInvalidO(self): self.assertInvalid('http://browsershots..org/')
    def testInvalidP(self): self.assertInvalid('http://browsershots.org/ ')
    def testInvalidQ(self): self.assertInvalid('http://.browsershots.org/')
    def testInvalidR(self): self.assertInvalid(' http://browsershots.org/')
    def testInvalidS(self): self.assertInvalid('http://1.2.3/')
    def testInvalidT(self): self.assertInvalid('http://1.2.3.4.5/')
    def testInvalidU(self): self.assertInvalid('http://1234.123.123.123/')
    def testInvalidV(self): self.assertInvalid('http://123.1234.123.123/')
    def testInvalidW(self): self.assertInvalid('http://123.123.1234.123/')
    def testInvalidX(self): self.assertInvalid('http://123.123.123.1234/')
    def testInvalidx(self): self.assertInvalid('http://123.123.123.123:abc/')

    def testValidA(self): self.assertValid('http://browsershots.org/')
    def testValida(self): self.assertValid('http://browsershots.org:80/')
    def testValidB(self): self.assertValid('https://browsershots.org/')
    def testValidb(self): self.assertValid('https://browsershots.org:443/')
    def testValidC(self): self.assertValid('http://www.browsershots.org/')
    def testValidD(self): self.assertValid('http://svn.browsershots.org/')
    def testValidE(self): self.assertValid('http://BrowserShots.org/')
    def testValidF(self): self.assertValid('http://WWW.BROWSERSHOTS.ORG/')
    def testValidf(self): self.assertValid('hTtP://WwW.BroWSersHotS.oRg/')
    def testValidG(self): self.assertValid('HTTP://BROWSERSHOTS.ORG/')
    def testValidH(self): self.assertValid('Https://browsershots.org/')
    def testValidI(self): self.assertValid('hTtps://browsershots.org/')
    def testValidJ(self): self.assertValid('htTps://browsershots.org/')
    def testValidK(self): self.assertValid('httPs://browsershots.org/')
    def testValidL(self): self.assertValid('httpS://browsershots.org/')
    def testValidM(self): self.assertValid('http://123.123.123.123/')
    def testValidN(self): self.assertValid('http://123.123.123.123/test/')
    def testValidO(self):
        self.assertValid('http://browsershots.org/index.html')
    def testValidP(self):
        self.assertValid('http://browsershots.org/robots.txt')
    def testValidQ(self):
        self.assertValid('http://browsershots.org/http://example.com/')
    def testValidR(self):
        self.assertValid('http://browsershots.org/?url=http://example.com/')
    def testValidS(self):
        self.assertValid('https://trac.browsershots.org/blog?format=rss')
