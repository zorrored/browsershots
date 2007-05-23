from psycopg import IntegrityError, ProgrammingError, DatabaseError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture
from shotserver04.platforms.models import Platform, OperatingSystem
from shotserver04.factories.models import Factory
from shotserver04.screenshots.models import Screenshot

VALID_SIZES = [
    (640, 480),
    (800, 600),
    (1024, 768),
    (1280, 1024),
    (1600, 1200),
    (640, 320),
    (800, 400),
    (1024, 512),
    (1280, 640),
    (1600, 800),
    (640, 5120),
    (800, 6400),
    (1024, 8192),
    (1280, 10240),
    (1600, 12800),
    ]

INVALID_SIZES = [
    (640, 319),
    (800, 399),
    (1024, 511),
    (1280, 639),
    (1600, 799),
    (640, 5121),
    (800, 6401),
    (1024, 8193),
    (1280, 10241),
    (1600, 12801),
    (0, 0),
    (639, 480),
    (1601, 1200),
    ]


class SizeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create()
        self.architecture = Architecture.objects.create()
        self.platform = Platform.objects.create()
        self.operating_system = OperatingSystem.objects.create(
            platform=self.platform)
        self.factory = Factory.objects.create(
            name='factory',
            admin=self.user,
            architecture=self.architecture,
            operating_system=self.operating_system)

    def tearDown(self):
        self.factory.delete()
        self.operating_system.delete()
        self.platform.delete()
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

    def testValidSizes(self):
        for width, height in VALID_SIZES:
            self.assertSizeValid(width, height)

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

    def testInvalidSizes(self):
        for width, height in INVALID_SIZES:
            self.assertSizeInvalid(width, height)
