from psycopg import IntegrityError, ProgrammingError, DatabaseError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture, OperatingSystem
from shotserver04.factories.models import Factory
from shotserver04.screenshots.models import Screenshot


class SizeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.architecture = Architecture.objects.create()
        self.operating_system_group = OperatingSystemGroup.objects.create()
        self.operating_system = OperatingSystem.objects.create(
            operating_system_group=self.operating_system_group,
            mobile=False)
        self.factory = Factory.objects.create(
            name='factory',
            admin=self.user,
            architecture=self.architecture,
            operating_system=self.operating_system)

    def tearDown(self):
        self.factory.delete()
        self.operating_system.delete()
        self.operating_system_group.delete()
        self.architecture.delete()
        self.user.delete()

    def assertSizeValid(self, width, height):
        try:
            screenshot = Screenshot.objects.create(
                hashkey='0123456789abcdef' * 2,
                factory=self.factory, message='',
                width=width, height=height)
            screenshot.delete()
        except IntegrityError:
            transaction.rollback()
            self.fail('could not create screenshot with valid size %dx%d' %
                      (width, height))

    def assertSizeInvalid(self, width, height):
        try:
            try:
                screenshot = Screenshot.objects.create(
                    hashkey='0123456789abcdef' * 2,
                    factory=self.factory, message='',
                    width=width, height=height)
                screenshot.delete()
                self.fail('created screenshot with invalid size %dx%d' %
                          (width, height))
            except IntegrityError:
                pass
        finally:
            transaction.rollback()

    def testSizeValid640(self): self.assertSizeValid(640, 480)
    def testSizeValid800(self): self.assertSizeValid(800, 600)
    def testSizeValid1024(self): self.assertSizeValid(1024, 768)
    def testSizeValid1280(self): self.assertSizeValid(1280, 1024)
    def testSizeValid1600(self): self.assertSizeValid(1600, 1200)

    def testSizeValidMin640(self): self.assertSizeValid(640, 320)
    def testSizeValidMin800(self): self.assertSizeValid(800, 400)
    def testSizeValidMin1024(self): self.assertSizeValid(1024, 512)
    def testSizeValidMin1280(self): self.assertSizeValid(1280, 640)
    def testSizeValidMin1600(self): self.assertSizeValid(1600, 800)

    def testSizeShort640(self): self.assertSizeInvalid(640, 319)
    def testSizeShort800(self): self.assertSizeInvalid(800, 399)
    def testSizeShort1024(self): self.assertSizeInvalid(1024, 511)
    def testSizeShort1280(self): self.assertSizeInvalid(1280, 639)
    def testSizeShort1600(self): self.assertSizeInvalid(1600, 799)

    def testSizeValidMax640(self): self.assertSizeValid(640, 5120)
    def testSizeValidMax800(self): self.assertSizeValid(800, 6400)
    def testSizeValidMax1024(self): self.assertSizeValid(1024, 8192)
    def testSizeValidMax1280(self): self.assertSizeValid(1280, 10240)
    def testSizeValidMax1600(self): self.assertSizeValid(1600, 12800)

    def testSizeLong640(self): self.assertSizeInvalid(640, 5121)
    def testSizeLong800(self): self.assertSizeInvalid(800, 6401)
    def testSizeLong1024(self): self.assertSizeInvalid(1024, 8193)
    def testSizeLong1280(self): self.assertSizeInvalid(1280, 10241)
    def testSizeLong1600(self): self.assertSizeInvalid(1600, 12801)

    def testSizeInvalid0(self): self.assertSizeInvalid(0, 0)
    def testSizeInvalidSmall(self): self.assertSizeInvalid(639, 480)
    def testSizeInvalidLarge(self): self.assertSizeInvalid(1601, 1200)
