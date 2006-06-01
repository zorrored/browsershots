# -*- coding: utf-8 -*-
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
System methods for introspection.
"""

__revision__ = '$Rev: 281 $'
__date__ = '$Date: 2006-06-01 07:57:09 +0200 (Thu, 01 Jun 2006) $'
__author__ = '$Author: johann $'

import re
from shotserver03 import xmlrpc

signature_match = re.compile(r'(\w+)\(([^\)]*)\)\s+=>\s+(\w+)').match

magic_names = {'listMethods': 'list_methods',
               'methodHelp': 'method_help',
               'methodSignature': 'method_signature'}

def list_methods():
    """
    list_methods() => array

    List all XML-RPC methods that this server supports.

    >>> list_methods()
    ('system.list_methods', 'system.method_help', 'system.method_signature')
    """
    return ('system.list_methods', 'system.method_help', 'system.method_signature')

def method_help(module_methodname):
    """
    method_help(string) => string

    Get the help text for an XML-RPC method.

    >>> method_help('system.method_help')
    'Get the help text for an XML-RPC method.'
    """
    modulename, methodname = xmlrpc.splitname(module_methodname)
    module, method = xmlrpc.module_method(modulename, methodname)
    dummy, doc = xmlrpc.split_docstring(methodname, method.__doc__)
    return doc

def method_signature(module_methodname):
    """
    method_signature(string) => array

    Get all possible signatures for an XML-RPC method. Each signature
    is an array of type names, the first entry of each signature is
    the method's return type.

    >>> method_signature('system.method_signature')
    [['array', 'string']]
    """
    modulename, methodname = xmlrpc.splitname(module_methodname)
    module, method = xmlrpc.module_method(modulename, methodname)
    lines, dummy = xmlrpc.split_docstring(methodname, method.__doc__)
    signatures = []
    for line in lines:
        match = signature_match(line)
        if match:
            name, args, result = match.groups()
            if module_methodname == name or module_methodname.endswith('.' + name):
                signature = [result]
                for arg in args.split(','):
                    signature.append(arg.strip())
                signatures.append(signature)
    return signatures

if __name__ == '__main__':
    import sys, doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
