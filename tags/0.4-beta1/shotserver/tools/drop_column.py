# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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
