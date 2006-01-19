#!/usr/bin/env python

# Browsershots
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
ATTENTION: any existing database named 'browsershots' will be dropped.
Create the database 'browsershots' with all tables. The root password
for mysql is read from /root/.my.cnf, so you may have to run this
script as root.
"""

__revision__ = '$Rev$'
__date__     = '$Date$'
__author__   = '$Author$'

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

# Simple variable length string tables.
for name in 'arch os browser engine'.split():
    cur.execute("""CREATE TABLE %s (
    id       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    value    VARCHAR(%u) NOT NULL UNIQUE)
    """ % (name, maxlen[name]))

# Users register online if they run a factory, or for priority service.
cur.execute("""CREATE TABLE `user` (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
nickname   VARCHAR(%(nickname)u),
email      VARCHAR(%(email)u) NOT NULL UNIQUE,
password   CHAR(41) NOT NULL,

updated    TIMESTAMP,
pwchanged  TIMESTAMP,
registered TIMESTAMP)
""" % maxlen)

# Users submit sites for testing.
cur.execute("""CREATE TABLE `site` (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
url        VARCHAR(%(url)u) NOT NULL,
user       INT UNSIGNED,
ip         INT UNSIGNED,

submitted  TIMESTAMP,

KEY (url),
KEY (user),
KEY (submitted))
""" % maxlen)

# For each site, a user can request different browsers.
cur.execute("""CREATE TABLE `job` (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
arch       INT UNSIGNED,
os         INT UNSIGNED,
os_version CHAR(10),

browser         INT UNSIGNED,
browser_version CHAR(10),
engine          INT UNSIGNED,
engine_version  CHAR(10),

width      SMALLINT UNSIGNED,
height     SMALLINT UNSIGNED,
depth      TINYINT UNSIGNED,

lang       CHAR(5),
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

KEY (browser, browserver),
KEY (engine, enginever),
KEY (factory),
KEY (uploaded))
""" % maxlen)

# Factories poll the job queue and upload screenshots.
cur.execute("""CREATE TABLE `factory` (
id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
nickname   VARCHAR(%(nickname)u) NOT NULL UNIQUE,
user       INT UNSIGNED NOT NULL,

arch       INT UNSIGNED NOT NULL,
os         INT UNSIGNED NOT NULL,
osversion  CHAR(10),
lang       CHAR(5),

updated    TIMESTAMP,
registered TIMESTAMP)
""" % maxlen)

# Factories poll the central server for jobs.
cur.execute("""CREATE TABLE `poll` (
factory    INT UNSIGNED NOT NULL,

useragent  VARCHAR(255),
browser    INT UNSIGNED NOT NULL,
browserver CHAR(10),
engine     INT UNSIGNED NOT NULL,
enginever  CHAR(10),

flash      TINYINT UNSIGNED NOT NULL,
java       TINYINT UNSIGNED NOT NULL,
javascript TINYINT UNSIGNED NOT NULL,
quicktime  TINYINT UNSIGNED NOT NULL,

width      SMALLINT UNSIGNED NOT NULL,
height     SMALLINT UNSIGNED NOT NULL,
depth      TINYINT UNSIGNED NOT NULL,

polled     TIMESTAMP)
""")

# Factories must lock jobs before processing.
cur.execute("""CREATE TABLE `lock` (
job     INT UNSIGNED PRIMARY KEY,
factory INT UNSIGNED NOT NULL,
locked  TIMESTAMP)
""")

# A nonce is a one-time challenge that can only be answered if you
# know the correct password, without disclosing the password even
# through an untrusted channel. Each factory can process many jobs in
# parallel, so it can hold many nonces. Users will be sent a nonce in
# email when they register or when they need to reset their password.
cur.execute("""CREATE TABLE `nonce` (
nonce   CHAR(32) PRIMARY KEY,
factory INT UNSIGNED,
user    INT UNSIGNED,

ip      INT UNSIGNED NOT NULL,

updated TIMESTAMP,
used    TIMESTAMP,
created TIMESTAMP)
""")

cur.close()
con.close()
