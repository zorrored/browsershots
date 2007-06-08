from psycopg import DatabaseError
from unittest import TestCase
from django.db import transaction
from shotserver04.platforms.models import OperatingSystem


class InvalidTestCase(TestCase):

    def testInvalidPlatform(self):
        try:
            self.assertRaises(DatabaseError, OperatingSystem.objects.create,
                              platform_id=-1)
        finally:
            transaction.rollback()
