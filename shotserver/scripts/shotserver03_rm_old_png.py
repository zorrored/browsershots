#! /usr/bin/python


"""
Delete screenshots that haven't been accessed in a long time.
"""


import os, time
from shotserver03 import database as db


png_path = '/var/www/browsershots.org/png'
subdirs = '140 180 240 450 full'.split()
timeout = 60 # days
now = time.time()
expire = now - timeout * 24 * 3600


def database_delete(filename):
    hashkey = filename[:32]
    cur.execute('DELETE FROM screenshot WHERE hashkey = %s', (hashkey, ))
    if cur.rowcount:
        print hashkey, 'deleted from database'


def files_delete(filename):
    for subdir in subdirs:
        path = os.path.join(png_path, subdir, prefix, filename)
        if os.path.exists(path):
            os.unlink(path)
            print path, 'deleted'


def find_expired(filelist):
    for filename in filelist:
        prefix = filename[:2]
        expired = True
        for subdir in subdirs:
            if subdir == '140':
                continue # because of recent dvd image
            path = os.path.join(png_path, subdir, prefix, filename)
            if os.path.exists(path):
                atime = os.stat(path).st_atime
                if atime > expire:
                    expired = False
                    break
            # else:
            #     print path, 'not found'
        if expired:
            database_delete(filename)
            files_delete(filename)


db.connect()
try:
    for index in range(256):
        prefix = '%02x' % index
        print 'checking', prefix
        filelist = ()
        for subdir in subdirs:
            path = os.path.join(png_path, subdir, prefix)
            if os.path.exists(path):
                candidate = os.listdir(path)
                if len(candidate) > len(filelist):
                    filelist = candidate
        find_expired(filelist)
finally:
    db.disconnect()
