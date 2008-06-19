#!/usr/bin/env python
import sys
import os
from glob import glob
import urllib
import re

SERVER_STATUS_URL = 'http://api.browsershots.org/server-status'
process_match = re.compile(r'<tr><td><b>\d+-\d+</b></td><td>(\d+)</td>').match
seconds_match = re.compile(r'</td><td>[\d\.]+</td><td>(\d+)</td>').match

# Get active processes
active = set()
status = urllib.urlopen(SERVER_STATUS_URL)
pid = None
seconds = {}
for line in status:
    previous_pid = pid
    pid = None
    if previous_pid:
        match = seconds_match(line)
        if match:
            seconds[previous_pid] = (
                seconds.get(previous_pid, 0) + int(match.group(1)))
    else:
        match = process_match(line)
        if match:
            pid = int(match.group(1))
            active.add(pid)

# Get all processes and parents
parents = set()
processes = []
for filename in glob('/proc/*/stat'):
    if not os.path.isfile(filename):
        continue
    parts = file(filename).read().split()
    pid, comm, state, ppid = parts[:4]
    if comm != '(apache2)':
        continue
    parents.add(int(ppid))
    utime, stime, cutime, cstime = parts[13:17]
    starttime, vsize, rss = parts[21:24]
    processes.append((starttime, int(pid), comm, state, ppid, utime, stime))
processes.sort()

for starttime, pid, comm, state, ppid, utime, stime in processes:
    print pid, comm, state, ppid, utime, stime, starttime,
    if pid in parents:
        print 'parent'
    elif pid in active and seconds[pid] > 20000:
        os.system('kill -9 %d' % pid)
        print 'KILLED', seconds[pid]
    elif pid in active:
        print 'active', seconds[pid]
    elif utime == stime == '0':
        print 'idle'
    else:
        os.system('kill -9 %d' % pid)
        print 'KILLED'
