#! /usr/bin/python
# -*- coding: utf-8 -*-
# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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
Create the database `browsershots` with all tables. Attention: any
existing database with that name will be dropped. The root password
for mysql is read from /root/.my.cnf, so you may have to run this
script as root.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import re
import MySQLdb
from shotserver.database import maxlen

re_key_value = re.compile(r'(\w+)\s*\=\s*(\S+)')
def read_credentials(filename = '/root/.my.cnf'):
    """
    Parse db admin and password from config file.
    """
    user = password = None
    for line in file(filename):
        m = re_key_value.match(line)
        if m is None:
            continue
        key, value = m.groups()
        if key == 'user':
            user = value
        if key == 'password':
            password = value
    if user is None:
        raise RuntimeError, 'no user found in %s' % filename
    if password is None:
        raise RuntimeError, 'no password found in %s' % filename
    return user, password

rootuser, rootpass = read_credentials()

# Create database.
db_name = 'browsershots'
con = MySQLdb.connect(host = 'localhost',
                       user = rootuser, passwd = rootpass)
cur = con.cursor()
cur.execute("DROP DATABASE IF EXISTS " + db_name)
cur.execute("CREATE DATABASE " + db_name)

# Set permissions.
cur.execute("GRANT USAGE, SELECT, INSERT, UPDATE, DELETE" +
               " ON `%s`.*" % db_name +
               " TO '%s'@'localhost'" % db_name +
               " IDENTIFIED BY 'secret'")

cur.close()
con.close()

# Create tables.
con = MySQLdb.connect(host = 'localhost', db = db_name,
                       user = rootuser, passwd = rootpass)
cur = con.cursor()

# Strings are stored in extra tables to avoid duplication.
def create_varchar_table(table, size):
    """
    Create a named string table.
    """
    cur.execute("""CREATE TABLE %s (
    id       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    value    VARCHAR(%u) NOT NULL UNIQUE,
    refcount INT UNSIGNED NOT NULL,

    updated  TIMESTAMP,
    added    TIMESTAMP)
    """ % (table, size))

create_varchar_table('nickname', maxlen['nickname'])
create_varchar_table('email', maxlen['email'])

create_varchar_table('url', 255)
create_varchar_table('arch', 10)
create_varchar_table('os', 20)
create_varchar_table('browser', 20)
create_varchar_table('engine', 20)

# Users register online if they run a factory, or for priority service.
cur.execute("DROP TABLE IF EXISTS user")
cur.execute("""CREATE TABLE user (
nickname   INT UNSIGNED PRIMARY KEY,
email      INT UNSIGNED NOT NULL UNIQUE,
password   CHAR(41) NOT NULL,

updated    TIMESTAMP,
pwchanged  TIMESTAMP,
registered TIMESTAMP)
""")

# Users submit jobs, factories process them.
cur.execute("DROP TABLE IF EXISTS job")
cur.execute("""CREATE TABLE job (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
url        INT UNSIGNED NOT NULL,
user       INT UNSIGNED NOT NULL,

arch       INT UNSIGNED,
os         INT UNSIGNED,
browser    INT UNSIGNED,
engine     INT UNSIGNED,
width      SMALLINT UNSIGNED,
height     SMALLINT UNSIGNED,
depth      TINYINT UNSIGNED,
lang       CHAR(4),
flash      TINYINT UNSIGNED,
java       TINYINT UNSIGNED,
javascript TINYINT UNSIGNED,

factory    INT UNSIGNED,
hashkey    CHAR(32) NOT NULL UNIQUE,
length     SMALLINT UNSIGNED,

updated    TIMESTAMP,
uploaded   TIMESTAMP,
redirected TIMESTAMP,
locked     TIMESTAMP,
submitted  TIMESTAMP,

KEY (url),
KEY (user),
KEY (browser),
KEY (width, height, depth),
KEY (factory),
KEY (uploaded),
KEY (submitted))
""")

# Factories must lock jobs before processing.
cur.execute("DROP TABLE IF EXISTS `lock`")
cur.execute("""CREATE TABLE `lock` (
job     INT UNSIGNED PRIMARY KEY,
factory INT UNSIGNED NOT NULL,
locked  TIMESTAMP)
""")

# Factories poll the job queue and upload screenshots.
cur.execute("DROP TABLE IF EXISTS factory")
cur.execute("""CREATE TABLE factory (
nickname   INT UNSIGNED PRIMARY KEY,
user       INT UNSIGNED NOT NULL,

arch       INT UNSIGNED NOT NULL,
os         INT UNSIGNED NOT NULL,
lang       CHAR(4),

updated    TIMESTAMP,
polled     TIMESTAMP,
uploaded   TIMESTAMP,
firstpoll  TIMESTAMP)
""")

# A nonce is a one-time challenge that can only be answered if you
# know the correct password, without disclosing the password even
# through an untrusted channel.
# Each factory can process many jobs in parallel, so it can hold many nonces.
# Users will be sent a nonce in email when they register or when they
# need to reset their password.
cur.execute("DROP TABLE IF EXISTS nonce")
cur.execute("""CREATE TABLE nonce (
nonce   CHAR(32) PRIMARY KEY,
factory INT UNSIGNED,
user    INT UNSIGNED,

ip      INT UNSIGNED NOT NULL,

updated TIMESTAMP,
used    TIMESTAMP,
created TIMESTAMP)
""")

# Each factory can have many browsers.
cur.execute("DROP TABLE IF EXISTS browser")
cur.execute("""CREATE TABLE browser (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
factory    INT UNSIGNED NOT NULL,

useragent  INT UNSIGNED NOT NULL,
browser    INT UNSIGNED NOT NULL,
engine     INT UNSIGNED NOT NULL,
flash      TINYINT UNSIGNED NOT NULL,
java       TINYINT UNSIGNED NOT NULL,
javascript TINYINT UNSIGNED NOT NULL,
quicktime  TINYINT UNSIGNED NOT NULL)
""")

# Each factory can have many screen resolutions.
cur.execute("DROP TABLE IF EXISTS resolution")
cur.execute("""CREATE TABLE resolution (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
factory    INT UNSIGNED NOT NULL,

width      SMALLINT UNSIGNED NOT NULL,
height     SMALLINT UNSIGNED NOT NULL,
depth      TINYINT UNSIGNED NOT NULL)
""")

cur.close()
con.close()
