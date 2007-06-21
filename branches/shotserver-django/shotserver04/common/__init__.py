# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Common utilities.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import xmlrpclib
import psycopg
from django.db import connection, transaction
from datetime import datetime, timedelta
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.functional import lazy

MAX_ATTEMPTS = 10
POLL_TIMEOUT = 10 # minutes
LOCK_TIMEOUT = 5 # minutes


def last_poll_timeout():
    """Factory is inactive if last poll was before this datetime."""
    return datetime.now() - timedelta(minutes=POLL_TIMEOUT)


def lock_timeout():
    """Request lock is expired if it was created before this datetime."""
    return datetime.now() - timedelta(minutes=LOCK_TIMEOUT)


def int_or_none(value):
    """Convert string to int, if possible."""
    if value.isdigit():
        return int(value)


def gettext_capfirst(text):
    """Translate and then change first letter to uppercase."""
    return capfirst(gettext(text))


lazy_gettext_capfirst = lazy(gettext_capfirst, str, unicode)


def get_or_fault(model, *args, **kwargs):
    """
    Get the specified object, or raise xmlrpclib.Fault with a detailed
    error message. Similar to django.shortcuts.get_object_or_404.
    """
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        filters = ' and '.join(
            ['%s=%s' % (key, kwargs[key]) for key in kwargs])
        raise xmlrpclib.Fault(0, '%s not found with %s.' % (
            model.__name__, filters))


def serializable(func):
    """
    Decorator that changes the PostgreSQL transaction isolation level
    to serializable. Use this for minimal functions that need to be
    isolated from concurrent access. The operation will be attempted
    again if a serialization error occurs (up to MAX_ATTEMPTS times).
    """

    @transaction.commit_manually
    def wrapper(*args, **kwargs):
        """
        Set the transaction isolation level to serializable, then run
        the wrapped function. Automatically retry on serialize error.
        """
        if transaction.is_dirty():
            transaction.commit()
        else:
            transaction.rollback()
        cursor = connection.cursor()
        for attempt in range(1, MAX_ATTEMPTS + 1):
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            try:
                result = func(*args, **kwargs)
                transaction.commit()
                return result
            except psycopg.ProgrammingError, error:
                serialize_error = "serialize access" in str(error).lower()
                if serialize_error and attempt < MAX_ATTEMPTS:
                    transaction.rollback()
                    # sys.stdout.write('!') # For test_overload.py
                else:
                    raise

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
