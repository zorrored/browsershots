#! /usr/bin/python
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
Delete screenshots that haven't been accessed in a long time.
"""

import os
import time
from shotserver03 import database as db

png_path = '/var/www/browsershots.org/png'
subdirs = '140 180 240 450 full'.split()
timeout = 10 # days
now = time.time()
expire = now - timeout * 24 * 3600


def database_delete(filename, counter):
    hashkey = filename[:32]
    cur.execute('DELETE FROM screenshot WHERE hashkey = %s', (hashkey, ))
    if cur.rowcount:
        counter['rows'] += cur.rowcount
        # print hashkey, 'deleted from database'


def files_delete(filename, counter):
    for subdir in subdirs:
        path = os.path.join(png_path, subdir, prefix, filename)
        if os.path.exists(path):
            os.unlink(path)
            counter['files'] += 1
            # print path, 'deleted'


def find_expired(filelist, counter):
    for filename in filelist:
        prefix = filename[:2]
        expired = True
        for subdir in subdirs:
            path = os.path.join(png_path, subdir, prefix, filename)
            if os.path.exists(path):
                atime = os.stat(path).st_atime
                if atime > expire:
                    expired = False
                    break
            # else:
            #     print path, 'not found'
        if expired:
            database_delete(filename, counter)
            files_delete(filename, counter)
    if counter['rows']:
        con.commit()


db.connect()
try:
    counter = {'files': 0, 'rows': 0}
    for index in range(256):
        prefix = '%02x' % index
        filelist = ()
        for subdir in subdirs:
            path = os.path.join(png_path, subdir, prefix)
            if os.path.exists(path):
                candidate = os.listdir(path)
                if len(candidate) > len(filelist):
                    filelist = candidate
        find_expired(filelist, counter)
        # print prefix
    if counter['rows'] or counter['files']:
        print 'deleted %s database rows and %s files' % (
            counter['rows'], counter['files'])
finally:
    db.disconnect()
