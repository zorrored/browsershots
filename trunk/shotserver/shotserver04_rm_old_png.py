#!/usr/bin/env python
# Delete old PNG files
#
# This script expects a list of candidates on stdin, like this:
# /var/www/v04.browsershots.org/png/160/74/749a5c7602d6de93d9a5bfdc2e7db1a9.png
# /var/www/v04.browsershots.org/png/160/74/742d8deb15f0cf2cd0a347f7dc3c58f7.png
# /var/www/v04.browsershots.org/png/160/74/7492c8add13e09205a3c788d47f9e599.png
#
# You can use the following command to find good candidates:
# find /var/www/v04.browsershots.org/png/160 -atime +10

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
import sys
import glob
import time
from shotserver04.screenshots.models import Screenshot

NOW = time.time()
EXPIRE_DAYS = 10
EXPIRE = NOW - EXPIRE_DAYS * 24 * 3600
FOLDERS = glob.glob('/var/www/v04.browsershots.org/png/*')


def png_filename(folder, hashkey):
    return os.path.join(folder, hashkey[:2], hashkey + '.png')


def _main():
    screenshot_count = unlink_count = 0
    for candidate in sys.stdin:
        basename = os.path.basename(candidate.rstrip())
        if len(basename) != 36:
            print basename, len(basename)
        hashkey = basename[:32]
        filenames = [png_filename(folder, hashkey) for folder in FOLDERS]
        filenames = filter(os.path.exists, filenames)
        if not filenames:
            continue
        atimes = [os.stat(filename).st_atime for filename in filenames]
        if max(atimes) > EXPIRE:
            continue
        # print chr(13), hashkey, len(atimes), max(atimes),
        # print 'delete', hashkey
        Screenshot.objects.filter(hashkey=hashkey).delete()
        screenshot_count += 1
        for filename in filenames:
            # print 'unlink', filename
            os.unlink(filename)
        unlink_count += len(filenames)
    print "deleted %d screenshots (%d files)" % (
        screenshot_count, unlink_count)


if __name__ == '__main__':
    # print EXPIRE
    _main()
