#!/usr/bin/env python
# Delete old PNG files

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
import sys
import glob
import time
from shotserver04.screenshots.models import Screenshot
from shotserver04.settings import PNG_ROOT

FOLDERS = glob.glob(os.path.join(PNG_ROOT, '*'))
CANDIDATE_FOLDER = os.path.join(PNG_ROOT, '160')
MAX_CANDIDATES = 5000
MIN_FREE_PERCENT = 10


def timestamp(when=None):
    return '%04d-%02d-%02d %02d:%02d:%02d' % time.localtime(when)[:6]


def disk_free_percent():
    stat = os.statvfs(PNG_ROOT)
    # total_disk_space = stat.f_blocks * stat.f_frsize
    # free_disk_space = stat.f_bavail * stat.f_frsize
    return 100.0 * stat.f_bavail / stat.f_blocks


def collect_candidates():
    print timestamp(), 'collecting...'
    hashkeys = []
    for dirname in os.listdir(CANDIDATE_FOLDER):
        dirname_full = os.path.join(CANDIDATE_FOLDER, dirname)
        if not os.path.isdir(dirname_full):
            continue
        # print dirname_full
        for pngname in os.listdir(dirname_full):
            if len(pngname) != 36:
                continue
            pngname_full = os.path.join(dirname_full, pngname)
            atime = os.stat(pngname_full).st_atime
            hashkey = pngname[:32]
            hashkeys.append((atime, hashkey))
    print timestamp(), 'found %d screenshots, sorting...' % len(hashkeys)
    hashkeys.sort()
    hashkeys = hashkeys[:MAX_CANDIDATES]
    return hashkeys


def hashkey_filenames(hashkey):
    return filter(os.path.exists,
        [os.path.join(folder, hashkey[:2], hashkey + '.png')
        for folder in FOLDERS])


def update_candidates(hashkeys):
    print timestamp(), 'updating...'
    for index in xrange(len(hashkeys)):
        atime, hashkey = hashkeys[index]
        max_atime = max([os.stat(filename).st_atime
            for filename in hashkey_filenames(hashkey)])
        if max_atime > atime:
            #print hashkey, timestamp(atime), timestamp(max_atime)
            hashkeys[index] = (max_atime, hashkey)
    print timestamp(), 'sorting again...'
    hashkeys.sort()


if __name__ == '__main__':
    free = disk_free_percent()
    if free > MIN_FREE_PERCENT:
        print '%.3f%% free, nothing to do' % free
        sys.exit(0)

    hashkeys = collect_candidates()
    last_atime = hashkeys[-1][0]
    update_candidates(hashkeys)

    screenshot_count = 0
    png_count = 0
    for atime, hashkey in hashkeys:
        if atime > last_atime:
            break
        free = disk_free_percent()
        if free > MIN_FREE_PERCENT:
            break
        print '%.3f' % free, hashkey, timestamp(atime)
        Screenshot.objects.filter(hashkey=hashkey).delete()
        screenshot_count += 1
        for filename in hashkey_filenames(hashkey):
            # print 'unlink', filename
            os.unlink(filename)
            png_count += 1
    print timestamp(), "deleted %d screenshots (%d files)" % (
        screenshot_count, png_count)
