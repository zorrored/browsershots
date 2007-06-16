#!/usr/bin/env python

"""
Extract SQL data from stdin and write each table to an SQL file.
"""

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
