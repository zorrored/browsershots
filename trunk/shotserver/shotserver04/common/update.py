# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Update only selected fields of a model.

The problem with model.save() is that it also overwrites all other
fields with possibly stale data.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import connection


def update_fields(instance, **kwargs):
    """
    """
    sql = ['UPDATE', connection.ops.quote_name(instance._meta.db_table), 'SET']
    field_names = [connection.ops.quote_name(f.column)
                   for f in instance._meta.fields]
    for field_name in kwargs:
        field = instance._meta.get_field(field_name)
        value = field.get_db_prep_save(kwargs[field_name])
        if isinstance(value, basestring):
            value = "'%s'" % value.encode('utf-8').replace('\\', r'\\')
        elif value is None:
            value = 'NULL'
        else:
            value = str(value)
        sql.extend((connection.ops.quote_name(field.column),
                    '=', value, ','))
    sql.pop(-1) # Remove the last comma
    sql.extend(['WHERE', 'id', '=', str(instance.id)])
    sql = ' '.join(sql)
    connection.cursor().execute(sql)
