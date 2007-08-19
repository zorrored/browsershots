#!/usr/bin/env python
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
usage: logdates.py <filename.log.1.gz> ...

Rename rotated compressed log files to include modification date.

The above example might be renamed to logfile.2005-08-31.gz which
makes it possible to use rsync on the log directory. Without this
little workaround, rsync will copy rotated files again and again
because the names change with each log rotation.

This script can be added to the postrotate script section in
/etc/logrotate.d/apache2 or similar.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import sys
import os
import time
import re

re_filename = re.compile(r'^(.+\.log)\.\d+\.(gz)$')
for filename in sys.argv[1:]:
    match = re_filename.match(filename)
    if match is None:
        continue
    name, suffix = match.groups()
    mtime = os.stat(filename).st_mtime
    date = time.strftime('%Y-%m-%d', time.localtime(mtime))
    newname = '%s.%s.%s' % (name, date, suffix)
    os.rename(filename, newname)
