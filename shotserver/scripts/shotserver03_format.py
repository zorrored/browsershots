#! /usr/bin/python

# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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
Check formatting of Python source code.
"""

__revision__ = '$Rev: 2 $'
__date__     = '$Date: 2006-02-26 14:02:33 +0100 (Sun, 26 Feb 2006) $'
__author__   = '$Author: johann $'

import sys, os

class FormatError:
    def __init__(self, filename, error):
        self.message = "error in %s: %s" % (filename, error)

def read_docstring(fh):
    lines = []
    while True:
        line = fh.readline()
        if not line: break
        lines.append(line)
        if line.strip() == '"""': break
    return ''.join(lines)

def read_block(fh):
    line = fh.readline()
    if line.startswith('"""'):
        return line + read_docstring(fh)
    lines = [line]
    while True:
        line = fh.readline()
        if not line: break
        if not line.strip(): break
        lines.append(line)
    return ''.join(lines)

def split_file(filename):
    fh = file(filename)
    shebang = read_block(fh)
    if shebang.startswith('#!'):
        head = read_block(fh)
    else:
        head = shebang
        shebang = ''
    docstring = read_block(fh)
    if fh.readline().strip():
        raise FormatError(filename, "no blank line after docstring")
    keywords = read_block(fh)
    return shebang, head, docstring, keywords

reference = split_file(sys.argv[0])
error = 0

files = sys.argv[1:]
files.sort()
for filename in files:
    try:
        shebang, head, docstring, keywords = split_file(filename)
        if shebang and shebang != reference[0]:
            raise FormatError(filename, "wrong shebang")
        if head != reference[1]:
            raise FormatError(filename, "wrong copyright")
        if not docstring.startswith('"""'):
            raise  FormatError(filename, "missing docstring")
        if not keywords.startswith("__revision__ = '$Rev:"):
            raise  FormatError(filename, "missing __revision__")
    except FormatError, f:
        print 'error:', f.message
        error = 1

if error:
    sys.exit(error)
