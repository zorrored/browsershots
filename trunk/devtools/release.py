#! /usr/bin/python


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
