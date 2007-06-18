# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
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
XML-RPC dispatcher with full introspection and multicall support.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
import xmlrpclib
from shotserver04.xmlrpc import register


class Dispatcher:
    """
    XML-RPC dispatcher with full introspection and multicall support.
    """

    def __init__(self, allow_none=False, encoding=None):
        self.funcs = {
            'system.listMethods': self.list_methods,
            'system.methodSignature': self.method_signature,
            'system.methodHelp': self.method_help,
            'system.multicall': self.multicall,
            }
        self.allow_none = allow_none
        self.encoding = encoding

    def register_function(self, function, name = None):
        """
        Registers a function to respond to XML-RPC requests.

        The optional name argument can be used to set a Unicode name
        for the function.
        """
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    @register(list)
    def list_methods(self, request):
        """
        Returns a list of the methods supported by the server.
        """
        methods = self.funcs.keys()
        methods.sort()
        return methods

    @register(list, str)
    def method_signature(self, request, method_name):
        """
        Returns a list describing the possible signatures of the
        method.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        if hasattr(method, '_signature'):
            result = []
            for x in method._signature:
                if x is None:
                    result.append('void')
                elif x is str:
                    result.append('string')
                else:
                    result.append(x.__name__)
            return [result]

    @register(str, str)
    def method_help(self, request, method_name):
        """
        Returns a string containing documentation for the specified
        method.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        lines = method.__doc__.splitlines()
        indent = min([len(line) - len(line.lstrip())
                      for line in lines if line.strip()])
        lines = [line[indent:] for line in lines]
        return '\n'.join(lines).strip()

    @register(list, list)
    def multicall(self, request, call_list):
        """
        Allows the caller to package multiple XML-RPC calls into a
        single request.
        """
        results = []
        for call in call_list:
            method = call['methodName']
            params = call['params']
            result = self.dispatch(method, request, params)
            results.append([result])
        return results

    def dispatch(self, method, request, params):
        """
        Call a registered XML-RPC method.
        """
        if not method in self.funcs:
            raise Exception('method "%s" is not supported' % method)
        func = self.funcs[method]
        response = func(request, *params)
        return (response, )

    def dispatch_and_marshal(self, method, request, params):
        """
        Call a registered XML-RPC method and marshal the response.
        """
        try:
            response = self.dispatch(method, request, params)
            response = xmlrpclib.dumps(response, methodresponse=True,
                allow_none=self.allow_none, encoding=self.encoding)
        except xmlrpclib.Fault, fault:
            response = xmlrpclib.dumps(fault,
                allow_none=self.allow_none, encoding=self.encoding)
        except:
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value)),
                allow_none=self.allow_none, encoding=self.encoding)
        return response

    def dispatch_request(self, request):
        """Unmarshal and run an XML-RPC request."""
        params, method = xmlrpclib.loads(request.raw_post_data)
        return self.dispatch_and_marshal(method, request, params)
