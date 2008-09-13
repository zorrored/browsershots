#!/usr/bin/env python
# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Generic command-line client for XML-RPC interfaces.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import os
import xmlrpclib
import re
from optparse import OptionParser
from pprint import pprint
from datetime import datetime

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

DEFAULT_SERVER = 'http://127.0.0.1:8000/xmlrpc/'


def read_password(filename):
    fields = {}
    pattern = re.compile(r'(\S+)="(\S+)"')
    for line in file(filename):
        attributes = dict(pattern.findall(line))
        if 'name' in attributes and 'value' in attributes:
            name = attributes['name']
            value = attributes['value']
            fields[name] = value
    return fields['username'], fields['password']


def authenticate(method, args, secret):
    args.append(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
    message = ' '.join([method] + [str(arg) for arg in args] + [secret])
    args.append(md5(message).hexdigest())


def _main():
    usage = "%prog [options] <module.method> [args] ..."
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print status messages, or debug with -vv")
    parser.add_option('-s', '--server', metavar='<url>',
                      help="server url (or XMLRPC_SERVER from environment)")
    parser.add_option('-a', '--auth', metavar='<filename>',
                      help="authenticate request with secret key")
    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error('method not specified, try system.listMethods')
    method = args.pop(0)
    if not options.server and 'XMLRPC_SERVER' in os.environ:
        options.server = os.environ['XMLRPC_SERVER']
    if not options.server:
        options.server = DEFAULT_SERVER
    if options.auth:
        name, password = read_password(options.auth)
        if len(args) == 0 or args[0] != name:
            parser.error("first argument must be %s" % name)
        authenticate(method, args, password)
    server = xmlrpclib.Server(options.server)
    func = server
    for part in method.split('.'):
        func = getattr(func, part)
    try:
        result = func(*args)
    except xmlrpclib.Fault, fault:
        print fault.faultCode, fault.faultString
        sys.exit(1)
    if isinstance(result, basestring):
        print result.rstrip()
    else:
        pprint(result)


if __name__ == '__main__':
    _main()
