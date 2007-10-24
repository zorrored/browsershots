#!/usr/bin/env python
# Simple test script for kill_memory_hogs.py.
#
# Allocate 400 MiB of RAM and go to sleep:
# memory_hog.py 400
#
# Then you can use the following to kill it:
# kill_memory_hogs.py 400

import sys
import time
from array import array

MEGS = int(sys.argv[1])
KILOBYTE = array('B', [0] * 1024)

a = array('B')
for meg in range(MEGS):
    for i in range(1024):
        a.extend(KILOBYTE)
    sys.stdout.write(str(meg + 1) + chr(13))
    sys.stdout.flush()

while True:
    time.sleep(1)
