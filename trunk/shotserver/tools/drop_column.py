# browsershots.org - Test your web design in different browsers
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
Drop a column from a SQL COPY.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys

headline = sys.stdin.readline()
headline = headline.replace(', request_id', '')
sys.stdout.write(headline)

while True:
    line = sys.stdin.readline()
    if not line:
        break
    if line.strip() == r'\.':
        sys.stdout.write(line)
        break
    values = line.rstrip('\n').split('\t')
    values.pop(2)
    sys.stdout.write('\t'.join(values) + '\n')
