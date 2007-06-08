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

import xmlrpclib
import psycopg
from django.db import connection, transaction

MAX_ATTEMPTS = 10


def get_or_fault(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        filters = ' and '.join(
            ['%s=%s' % (key, kwargs[key]) for key in kwargs])
        raise xmlrpclib.Fault(0, '%s not found with %s.' % (
            model.__name__, filters))


def serializable(func):

    @transaction.commit_manually
    def wrapper(*args, **kwargs):
        if transaction.is_dirty():
            transaction.commit()
        cursor = connection.cursor()
        for attempt in range(1, MAX_ATTEMPTS + 1):
            cursor.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
            try:
                result = func(*args, **kwargs)
                transaction.commit()
                return result
            except Exception, error:
                transaction.rollback()
                serialize_failed = (
                    isinstance(error, psycopg.ProgrammingError) and
                    error.message.lower().count("serialize access"))
                if attempt == MAX_ATTEMPTS or not serialize_failed:
                    raise

    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
