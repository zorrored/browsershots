#!/usr/bin/env python
# Kill memory hogs (runaway processes that take up all memory).
# This is a useful workaround when some processes start to misbehave.
#
# To check for processes over 300 MiB once every minute, add the
# following line to your /etc/crontab (without the # sign):
# * *	* * *	root	kill_memory_hogs.py 300

import sys
import commands

if len(sys.argv) == 2:
    MAXIMUM_VIRTUAL_SIZE = int(sys.argv[-1]) # mebibytes
else:
    MAXIMUM_VIRTUAL_SIZE = 200 # mebibytes

processes = commands.getoutput('ps -eo vsize=,pid=,args=')
for process in processes.splitlines():
    parts = process.split()
    if len(parts) < 3:
        print 'expected 3 or more words:', process
        continue
    if parts[0].isdigit():
        vsize = int(parts[0])
    else:
        print 'expected integer for first word:', process
        continue
    if parts[1].isdigit():
        pid = int(parts[1])
    else:
        print 'expected integer for second word:', process
        continue
    megs = vsize / 1024.0
    if megs <= MAXIMUM_VIRTUAL_SIZE:
        continue
    rest = ' '.join(parts[2:])
    text = '%s (%.1f MiB, pid %d)' % (rest, megs, pid)
    status, output = commands.getstatusoutput('kill -9 %d' % pid)
    if status:
        print 'could not kill', text
        print output
    else:
        print 'killed', text
