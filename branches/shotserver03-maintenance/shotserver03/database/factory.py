# browsershots.org ShotServer 0.3-beta1
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
Database interface for factory table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"


def name_to_serial(name):
    """
    Get the serial number from the database.
    """
    cur.execute("SELECT factory FROM factory WHERE name=%s", (name, ))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    raise KeyError(name)


def serial_to_name(serial):
    """
    Get the factory name from the database.
    """
    cur.execute("SELECT name FROM factory WHERE factory=%s", (serial, ))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    raise KeyError(serial)


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
    # Factory options
    cur.execute("""\
SELECT opsys_group.name
FROM factory
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
WHERE factory = %s
""", (factory, ))
    opsys_name = cur.fetchone()[0]
    where = ["(opsys_group IS NULL OR opsys_group.name = '%s')" % opsys_name]

    # Match browsers names and versions
    cur.execute("""\
SELECT DISTINCT browser_group.name, major, minor
FROM factory_browser
JOIN browser_group USING (browser_group)
WHERE factory = %s
AND factory_browser.disabled IS NULL
""", (factory, ))
    alternatives = []
    for row in cur.fetchall():
        alternatives.append("(browser_group.name = '%s'" % row[0]
                            + " AND (major IS NULL OR major = %d)" % row[1]
                            + " AND (minor IS NULL OR minor = %d))" % row[2])
    where.append('(%s)' % ' OR '.join(alternatives))

    # Match screen resolutions
    cur.execute("""
SELECT DISTINCT width
FROM factory_screen
WHERE factory = %s
""", (factory, ))
    alternatives = ['width IS NULL']
    for row in cur.fetchall():
        width = row[0]
        alternatives.append('width = %d' % width)
    where.append('(%s)' % ' OR '.join(alternatives))

    # Unspecified request options will always match
    namedict = {}
    for name in 'bpp js java flash media'.split():
        namedict[name] = ['%s IS NULL' % name]

    # Match factory features
    cur.execute("""
SELECT name, intval, strval
FROM factory_feature
WHERE factory = %s
""", (factory, ))
    for name, intval, strval in cur.fetchall():
        if intval is not None:
            clause = "%s = %d" % (name, intval)
        elif strval is not None:
            clause = "'%s' LIKE %s" % (strval, name)
        else:
            continue
        namedict[name].append(clause)
    for name, alternatives in namedict.iteritems():
        where.append('(%s)' % ' OR '.join(alternatives))
    return ' AND '.join(where)


def select_active():
    """
    List active factories.
    """
    cur.execute("""\
SELECT factory, factory.name, person.nickname,
       opsys_group.name, distro, major, minor, codename,
       extract(epoch from last_poll)::bigint AS last_poll,
       extract(epoch from last_upload)::bigint AS last_upload,
       per_hour, per_day
FROM factory
JOIN person ON (factory.owner = person.person)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
WHERE last_upload>NOW()-'48:00'::interval
ORDER BY per_day DESC, last_upload DESC
""")
    return cur.fetchall()


def select_by_owner(owner):
    """
    List factories with a given administrator.
    """
    cur.execute("""\
SELECT factory, factory.name, person.nickname,
       opsys_group.name, distro, major, minor, codename,
       extract(epoch from last_poll)::bigint AS last_poll,
       extract(epoch from last_upload)::bigint AS last_upload,
       per_hour, per_day
FROM factory
JOIN person ON (factory.owner = person.person)
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
WHERE owner = %s
ORDER BY factory.name
""" % (owner, ))
    return cur.fetchall()


def update_last_poll(factory):
    """Set the last poll timestamp to NOW()."""
    cur.execute("""\
UPDATE factory
SET last_poll = NOW()
WHERE factory = %s
""", (factory, ))


def update_last_upload(factory):
    """Set the last upload timestamp to NOW()."""
    cur.execute("""\
UPDATE factory
SET last_upload = NOW()
WHERE factory = %s
""", (factory, ))


def info(factory):
    """Get some information about this factory."""
    cur.execute("""\
SELECT factory.name, opsys_group.name, distro, major, minor, codename,
architecture.name, to_char(factory.created, 'YYYY-MM-DD'), person.nickname
FROM factory
JOIN opsys USING (opsys)
JOIN opsys_group USING (opsys_group)
JOIN architecture USING (architecture)
JOIN person on person=factory.creator
WHERE factory = %s
""", (factory, ))
    return cur.fetchone()
