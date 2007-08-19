#!/usr/bin/env python
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
Extract SQL data from stdin and write each table to an SQL file.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys


def copy_table(line):
    table = line.split()[1]
    outfile = open('%s.sql' % table, 'w')
    outfile.write(line)
    while line.strip() != r'\.':
        line = sys.stdin.readline()
        outfile.write(line)
    outfile.write("""
SELECT '%s' AS table_name,
setval('%s_id_seq', (
    SELECT max(id) FROM %s
)) as pkey_max;
""" % (table, table, table))
    outfile.close()


if __name__ == '__main__':
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        if line.startswith('COPY '):
            copy_table(line)
