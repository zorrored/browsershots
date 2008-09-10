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

import os
import xmlrpclib
from optparse import OptionParser
from pprint import pprint

DEFAULT_SERVER = 'http://127.0.0.1:8000/xmlrpc/'


def _main():
    usage = "%prog [options] <module.method> [args] ..."
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print status messages, or debug with -vv")
    parser.add_option('-s', '--server', metavar='<url>',
                      help="server url (or XMLRPC_SERVER from environment)")
    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error('method not specified, try system.listMethods')
    method = args.pop(0)
    if not options.server:
        if 'XMLRPC_SERVER' in os.environ:
            options.server = os.environ['XMLRPC_SERVER']
    if not options.server:
        options.server = DEFAULT_SERVER
    server = xmlrpclib.Server(options.server)
    func = server
    for part in method.split('.'):
        func = getattr(func, part)
    pprint(func(*args))


if __name__ == '__main__':
    _main()
