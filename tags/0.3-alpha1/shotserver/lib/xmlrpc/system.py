# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
System methods for introspection.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03 import xmlrpc

# A list of methods to export through XML-RPC.
export_methods = ['listMethods', 'methodHelp', 'methodSignature']

# Mapping virtual names to actual functions.
magic_names = {'listMethods': 'list_methods',
               'methodHelp': 'method_help',
               'methodSignature': 'method_signature'}

def list_methods():
    """
    list_methods() => array
    List all XML-RPC methods that this server supports.
    >>> type(list_methods()) is list
    True
    >>> len(list_methods()) > 2
    True
    """
    result = []
    for modulename in xmlrpc.export_modules:
        module = xmlrpc.import_deep('shotserver03.xmlrpc.' + modulename)
        assert hasattr(module, 'export_methods')
        for methodname in module.export_methods:
            result.append(modulename + '.' + methodname)
    return result

def method_signature(module_methodname):
    """
    method_signature(string) => array
    Get all possible signatures for an XML-RPC method. Each signature
    is an array of type names, the first entry of each signature is
    the method's return type.
    >>> method_signature('system.method_signature')
    [['array', 'string']]
    """
    dummy, method = xmlrpc.module_method(module_methodname)
    return xmlrpc.split_docstring(method.__doc__)[0]

def method_help(module_methodname):
    """
    method_help(string) => string
    Get the help text for an XML-RPC method.
    >>> method_help('system.method_help')
    'Get the help text for an XML-RPC method.'
    """
    dummy, method = xmlrpc.module_method(module_methodname)
    return xmlrpc.split_docstring(method.__doc__)[1]

if __name__ == '__main__':
    import sys, doctest
    errors, tests = doctest.testmod()
    if errors:
        sys.exit(1)
