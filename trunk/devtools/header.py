#!/usr/bin/env python
# pep8.py - Check Python source code formatting, according to PEP 8
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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

"""
Adjust comment header in a batch of source files.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

import sys


def remove_shebang(lines):
    result = []
    if lines[0].startswith('#!'):
        result.append(lines.pop(0))
    if lines[0].count(' coding: '):
        result.append(lines.pop(0))
    return result


def remove_comment(lines):
    result = []
    while lines[0].startswith('#'):
        result.append(lines.pop(0))
    return result


def adjust_lines(lines, header):
    shebang = remove_shebang(lines)
    old_header = remove_comment(lines)
    lines[0:0] = shebang + header
    return header != old_header


def adjust_file(filename, header):
    lines = file(filename).readlines()
    if adjust_lines(lines, header):
        print filename
        file(filename, 'w').write(''.join(lines))


def adjust_files(filenames, header):
    filenames.sort()
    for filename in filenames:
        adjust_file(filename, header)


def _main():
    reference = file(sys.argv[1]).readlines()
    shebang = remove_shebang(reference)
    # print 'shebang', shebang
    header = remove_comment(reference)
    # print 'header', header
    adjust_files(sys.argv[2:], header)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Copy header comment from one file to many others."
        print "usage: %s <from-file> <to-file-1> <to-file-2> ..."
    else:
        _main()
