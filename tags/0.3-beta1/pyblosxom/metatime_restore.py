#! /usr/bin/python
# metatime_restore.py
# Copyright 2006 Johann C. Rocholl <johann@rocholl.net>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Inspired by the unmaintained metadate plugin (Error 403 for
# http://www.binaryuprising.com/code/pyblosxom/metadate.py on
# 2006-08-12).


"""
If a file contains a line like the following, this tool changes the
filesystem mtime of the file to the saved value.

#metatime 2006-06-12T16:59:38Z
"""


import sys, os, re, time


timestamp_match = re.compile(r'#metatime\s+' +
                             r'(\d{4})-(\d{2})-(\d{2})T' +
                             r'(\d{2}):(\d{2}):(\d{2})Z').match


def read_metatime(filename):
    """
    Read the mtime from an entry's metadata.
    """
    infile = file(filename)
    title = infile.readline()
    while True:
        line = infile.readline()
        if not line.startswith('#'):
            break
        match = timestamp_match(line)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            hour = int(match.group(4))
            minute = int(match.group(5))
            second = int(match.group(6))
            timetuple = (year, month, day,
                         hour, minute, second,
                         0, 0, -1)
            return time.mktime(timetuple)


def _main(filenames):
    """
    Reset mtime to metatime if available.
    """
    for filename in filenames:
        mtime = read_metatime(filename)
        if mtime is None:
            print "no #mtime in", filename
            continue
        os.utime(filename, (mtime, mtime))


if __name__ == '__main__':
    _main(sys.argv[1:])
