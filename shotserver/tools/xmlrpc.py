#!/usr/bin/env python

import os
import xmlrpclib
from optparse import OptionParser
from pprint import pprint

DEFAULT_SERVER = 'http://127.0.0.1:8000/xmlrpc/'


def _main():
    usage = "%prog [options] method [args] ..."
    parser = OptionParser(usage)
    parser.add_option('-v', '--verbose', default=0, action='count',
                      help="print status messages, or debug with -vv")
    parser.add_option('-s', '--server', metavar='<url>',
                      help="server url (or XMLRPC_SERVER from environment)")
    options, args = parser.parse_args()
    if len(args) == 0:
        parser.error('method not specified')
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
