from psycopg import IntegrityError
from unittest import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from shotserver04.factories.models import (
    Factory, Architecture, ScreenSize, ColorDepth,
    OperatingSystemGroup, OperatingSystem)


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
        transaction.commit()

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
        transaction.commit()

    def testFactoryName(self):
        self.factory.name = 'factory'
        self.factory.save()
        transaction.commit()
        self.assertEqual(len(Factory.objects.filter(name='factory')), 1)

    def testFactoryNameEmpty(self):
        self.factory.name = ''
        self.assertRaises(IntegrityError, self.factory.save)
        transaction.rollback()

    def testFactoryNameInvalid(self):
        self.factory.name = '-'
        self.assertRaises(IntegrityError, self.factory.save)
        transaction.rollback()

    def testFactoryCreateDuplicate(self):
        self.assertRaises(IntegrityError, Factory.objects.create,
                          name='factory', admin=self.user,
                          architecture=self.architecture,
                          operating_system=self.operating_system)
        transaction.rollback()

    def testFactoryCreateEmpty(self):
        self.assertRaises(IntegrityError, Factory.objects.create,
                          admin=self.user,
                          architecture=self.architecture,
                          operating_system=self.operating_system)
        transaction.rollback()

    def testFactoryCreateInvalid(self):
        self.assertRaises(IntegrityError, Factory.objects.create,
                          name='-', admin=self.user,
                          architecture=self.architecture,
                          operating_system=self.operating_system)
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
        self.assertRaises(IntegrityError, ScreenSize.objects.create,
                          factory=self.factory, width=800, height=600)
        transaction.rollback()

    def testColorDepth(self):
        queryset = self.factory.colordepth_set
        self.assertEqual(len(queryset.all()), 2)

    def testColorDepthDuplicate(self):
        self.assertRaises(IntegrityError, ColorDepth.objects.create,
                          factory=self.factory, bits_per_pixel=24)
        transaction.rollback()
