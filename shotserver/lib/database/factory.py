# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Database interface for factory table.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

def select_serial(name):
    """
    Get the serial number from the database.
    """
    cur.execute("SELECT factory FROM factory WHERE name=%s", (name, ))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    raise KeyError("factory.name=%s" % name)

def select_salt(factory):
    """
    Get the password salt for a factory.
    If there's no factory password, get the factory owner's salt.
    """
    cur.execute("""\
SELECT factory.salt, owner.salt
FROM factory
JOIN person AS owner ON factory.owner = owner.person
WHERE factory = %s
""", (factory, ))
    factory_salt, owner_salt = cur.fetchone()
    if factory_salt is None:
        return owner_salt
    return factory_salt

def features(factory):
    """
    Get a WHERE clause that matches jobs for a given factory.
    """
    where = []
    # Match screen resolutions
    cur.execute("SELECT DISTINCT width FROM factory_screen WHERE factory = %s", (factory, ))
    alternatives = ['width IS NULL']
    for row in cur.fetchall():
        width = row[0]
        alternatives.append('width = %d' % width)
    where.append('(%s)' % ' OR '.join(alternatives))
    # Match factory features
    cur.execute("SELECT name, intval, strval FROM factory_feature WHERE factory = %s", (factory, ))
    namedict = {}
    for name, intval, strval in cur.fetchall():
        if intval is not None:
            clause = "%s = %d" % (name, intval)
        elif strval is not None:
            clause = "'%s' LIKE %s" % (strval, name)
        else:
            continue
        alternatives = namedict.get(name, [])
        alternatives.append(clause)
        namedict[name] = alternatives
    for name, alternatives in namedict.iteritems():
        if len(alternatives) == 0:
            continue
        alternatives.insert(0, '%s IS NULL' % name)
        where.append('(%s)' % ' OR '.join(alternatives))
    return ' AND '.join(where)
