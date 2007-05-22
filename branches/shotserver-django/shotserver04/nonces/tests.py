from unittest import TestCase
from psycopg import IntegrityError, ProgrammingError, DatabaseError
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.nonces.models import Nonce
from shotserver04.platforms.models import Architecture, OperatingSystem
from shotserver04.factories.models import Factory


class NonceTestCase(TestCase):

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

    def testInvalidFactoryForNonce(self):
        try:
            self.assertRaises(DatabaseError, Nonce.objects.create,
                              factory_id=-1)
        finally:
            transaction.rollback()
