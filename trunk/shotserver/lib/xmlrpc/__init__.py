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
XML-RPC request handler.
"""

__revision__ = '$Rev: 281 $'
__date__ = '$Date: 2006-06-01 07:57:09 +0200 (Thu, 01 Jun 2006) $'
__author__ = '$Author: johann $'

import xmlrpclib, re

explain_xmlrpc = """\
Your user agent did not send a valid XML-RPC request.
Use an XML-RPC client to access this resource.
The following is an example client in Python.

import sys, xmlrpclib
url = sys.argv[1]
server = xmlrpclib.Server(url)
for method in server.system.listMethods():
    for signature in server.system.methodSignature(method):
        signature = ', '.join(signature)
        print "%s(%s)" % (method, signature)
    print server.system.methodHelp(method)
    print
"""

def import_deep(name):
    """
    Import a module from some.levels.deep and return the module
    itself, not its uppermost parent.
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def splitname(module_methodname):
    """Split the module from a qualified method name."""
    return module_methodname.rsplit('.', 1)

def module_method(modulename, methodname):
    """
    Import a module and method by string names.
    If the module has magic names, these will be considered.
    """
    module = import_deep('shotserver03.xmlrpc.%s' % modulename)
    if hasattr(module, 'magic_names'):
        if module.magic_names.has_key(methodname):
            methodname = module.magic_names[methodname]
    assert hasattr(module, methodname)
    method = getattr(module, methodname)
    return module, method

whitespace_match = re.compile(r'\n*([\s\t]*)').match
def split_docstring(methodname, doc):
    """
    split_docstring(string) => array

    Split a docstring into signature lines and documentation.
    Remove indentation and doctest dialogue.

    >>> split_docstring('split_docstring')
    (['split_docstring(string) => array'], 'Split a docstring into signature lines and documentation.
    Remove indentation and doctest dialogue.')
    """
    whitespace = whitespace_match(doc).group(1)
    if whitespace:
        doc = doc.replace('\n'+whitespace, '\n')
    doc = doc.strip()
    lines = doc.split('\n')
    signatures = []
    doc = []
    while lines[0].startswith(methodname + '('):
        signatures.append(lines.pop(0).strip())
    while lines and not lines[0].startswith('>>>'):
        doc.append(lines.pop(0))
    doc = '\n'.join(doc).strip()
    return signatures, doc

def handler(req):
    """
    Handler for XML-RPC requests.
    """
    from mod_python import apache
    data = req.read()
    if not data:
        req.content_type = 'text/plain'
        req.write(explain_xmlrpc)
        return apache.OK
    params, methodname = xmlrpclib.loads(data)
    modulename, methodname = splitname(methodname)
    module, method = module_method(modulename, methodname)
    answer = method(*params)
    answer = xmlrpclib.dumps((answer, ), methodresponse = True)
    req.write(answer)
    return apache.OK
