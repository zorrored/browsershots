from psycopg import IntegrityError, ProgrammingError, DatabaseError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.factories.models import (
    Factory, Architecture, ScreenSize, ColorDepth,
    OperatingSystemGroup, OperatingSystem, Nonce)


class FactoriesTestCase(TestCase):

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
        self.size_640 = ScreenSize.objects.create(
            factory=self.factory, width=640, height=480)
        self.size_800 = ScreenSize.objects.create(
            factory=self.factory, width=800, height=600)
        self.size_1024 = ScreenSize.objects.create(
            factory=self.factory, width=1024, height=768)
        self.depth_16 = ColorDepth.objects.create(
            factory=self.factory, bits_per_pixel=16)
        self.depth_24 = ColorDepth.objects.create(
            factory=self.factory, bits_per_pixel=24)

    def tearDown(self):
        self.depth_16.delete()
        self.depth_24.delete()
        self.size_640.delete()
        self.size_800.delete()
        self.size_1024.delete()
        self.factory.delete()
        self.operating_system.delete()
        self.operating_system_group.delete()
        self.architecture.delete()
        self.user.delete()

    def testFactoryName(self):
        self.factory.name = 'factory'
        self.factory.save()
        self.assertEqual(len(Factory.objects.filter(name='factory')), 1)

    def testFactoryNameEmpty(self):
        try:
            self.factory.name = ''
            self.assertRaises(IntegrityError, self.factory.save)
        finally:
            transaction.rollback()

    def testFactoryNameInvalid(self):
        try:
            self.factory.name = '-'
            self.assertRaises(IntegrityError, self.factory.save)
        finally:
            transaction.rollback()

    def testFactoryCreateDuplicate(self):
        try:
            self.assertRaises(IntegrityError, Factory.objects.create,
                              name='factory', admin=self.user,
                              architecture=self.architecture,
                              operating_system=self.operating_system)
        finally:
            transaction.rollback()

    def testFactoryCreateEmpty(self):
        try:
            self.assertRaises(IntegrityError, Factory.objects.create,
                              admin=self.user,
                              architecture=self.architecture,
                              operating_system=self.operating_system)
        finally:
            transaction.rollback()

    def testFactoryCreateInvalid(self):
        try:
            self.assertRaises(IntegrityError, Factory.objects.create,
                              name='-', admin=self.user,
                              architecture=self.architecture,
                              operating_system=self.operating_system)
        finally:
            transaction.rollback()

    def testScreenSize(self):
        queryset = self.factory.screensize_set
        self.assertEqual(len(queryset.all()), 3)
        self.assertEqual(len(queryset.filter(width=800)), 1)
        self.assertEqual(len(queryset.filter(width__exact=800)), 1)
        self.assertEqual(len(queryset.filter(width__gte=800)), 2)
        self.assertEqual(len(queryset.filter(width__lte=800)), 2)
        self.assertEqual(len(queryset.filter(width__gt=800)), 1)
        self.assertEqual(len(queryset.filter(width__lt=800)), 1)

    def testScreenSizeDuplicate(self):
        try:
            self.assertRaises(IntegrityError, ScreenSize.objects.create,
                              factory=self.factory, width=800, height=600)
        finally:
            transaction.rollback()

    def testColorDepth(self):
        queryset = self.factory.colordepth_set
        self.assertEqual(len(queryset.all()), 2)

    def testColorDepthDuplicate(self):
        try:
            self.assertRaises(IntegrityError, ColorDepth.objects.create,
                              factory=self.factory, bits_per_pixel=24)
        finally:
            transaction.rollback()

    def assertNonceValid(self, hashkey):
        try:
            try:
                nonce = Nonce.objects.create(factory=self.factory,
                    hashkey=hashkey, ip='127.0.0.1')
                nonce.delete()
            except (IntegrityError, ProgrammingError):
                self.fail("could not create nonce with valid hashkey '%s'" %
                          hashkey)
        finally:
            transaction.rollback()

    def assertNonceInvalid(self, hashkey):
        try:
            try:
                nonce = Nonce.objects.create(factory=self.factory,
                    hashkey=hashkey, ip='127.0.0.1')
                nonce.save()
                nonce.delete()
                self.fail("created nonce with invalid hashkey '%s'" % hashkey)
            except (IntegrityError, ProgrammingError):
                pass
        finally:
            transaction.rollback()

    def testNonceValidA(self):
        self.assertNonceValid('12345678901234567890123456789012')
    def testNonceValidB(self):
        self.assertNonceValid('a234b6789012c4567d90123e56789f12')
    def testNonceValidC(self):
        self.assertNonceValid('0a234b6789012c4567d90123e56789ff')

    def testNonceInvalidA(self):
        self.assertNonceInvalid('1234567890123456789012345678901')
    def testNonceInvalidB(self):
        self.assertNonceInvalid('a234b6789012c4567d90123e56789f123')
    def testNonceInvalidC(self):
        self.assertNonceInvalid('0a234b6789012c4567d90123e56789fg')

    def testNonceDuplicate(self):
        try:
            hashkey = '0123456789abcdef' * 2
            nonce = Nonce.objects.create(hashkey=hashkey,
                factory=self.factory, ip='127.0.0.1')
            self.assertRaises(IntegrityError, Nonce.objects.create,
                hashkey=hashkey, factory=self.factory, ip='127.0.0.1')
        finally:
            transaction.rollback()


class ForeignKeyTestCase(TestCase):

    def testInvalidArchitecture(self):
        try:
            self.assertRaises(DatabaseError, Factory.objects.create,
                              architecture_id=-1)
        finally:
            transaction.rollback()

    def testInvalidOperatingSystemGroup(self):
        try:
            self.assertRaises(DatabaseError, OperatingSystem.objects.create,
                              operating_system_group_id=-1)
        finally:
            transaction.rollback()

    def testInvalidOperatingSystem(self):
        try:
            self.assertRaises(DatabaseError, Factory.objects.create,
                              operating_system_id=-1)
        finally:
            transaction.rollback()

    def testInvalidAdmin(self):
        try:
            self.assertRaises(DatabaseError, Factory.objects.create,
                              admin_id=-1)
        finally:
            transaction.rollback()

    def testInvalidFactoryForScreenSize(self):
        try:
            self.assertRaises(DatabaseError, ScreenSize.objects.create,
                              factory_id=-1, width=800, height=600)
        finally:
            transaction.rollback()

    def testInvalidFactoryForColorDepth(self):
        try:
            self.assertRaises(DatabaseError, ColorDepth.objects.create,
                              factory_id=-1, bits_per_pixel=24)
        finally:
            transaction.rollback()

    def testInvalidFactoryForNonce(self):
        try:
            self.assertRaises(DatabaseError, Nonce.objects.create,
                              factory_id=-1)
        finally:
            transaction.rollback()
