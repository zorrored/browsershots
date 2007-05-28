#! /usr/bin/python
# release.py - Make ZIP files for software releases
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
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

import sys
import os
import re


def error(message, code = 1):
    print message.strip()
    sys.exit(code)


def shell(command):
    print command
    code = os.system(command)
    if code:
        error('failed with exit code %d' % code, code / 256)


if len(sys.argv) < 3:
    error("""\
usage: release.py <version> <packages>
example: release.py 0.3-alpha1 shotserver shotfactory
""")


version = sys.argv[1]
for package in sys.argv[2:]:
    package = package.strip('/')
    if package.count('/'):
        error('package "%s" contains a slash' % package)
    package_version = package + '-' + version
    zip_filename = package_version + '.zip'
    shell('rm -rf %s %s' % (package_version, zip_filename))
    shell('cp -r %s %s' % (package, package_version))
    shell('find %s -name .svn | xargs rm -rf' % package_version)
    shell('find %s -name "*.rej" | xargs rm -f' % package_version)
    shell('find %s -name "shotfactory.log" | xargs rm -f' % package_version)
    shell('find %s -name "screenlog.0" | xargs rm -f' % package_version)
    shell('find %s -name "\#*\#" | xargs rm -f' % package_version)
    shell('zip -qr %s %s' % (zip_filename, package_version))
