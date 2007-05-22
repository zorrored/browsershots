from psycopg import IntegrityError, ProgrammingError, DatabaseError
from unittest import TestCase
from django.db import transaction
from shotserver04.platforms.models import Architecture
from shotserver04.platforms.models import Platform, OperatingSystem


class InvalidTestCase(TestCase):

    def testInvalidPlatform(self):
        try:
            self.assertRaises(DatabaseError, OperatingSystem.objects.create,
                              platform_id=-1)
        finally:
            transaction.rollback()
