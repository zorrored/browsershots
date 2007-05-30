# Inspired by SimpleXMLRPCServer.py by Brian Quinlan (brian@sweetapp.com).

import sys
import xmlrpclib
from shotserver04.xmlrpc import signature


class Dispatcher:

    def __init__(self, allow_none=False, encoding=None):
        self.funcs = {
            'system.listMethods': self.system_listMethods,
            'system.methodSignature': self.system_methodSignature,
            'system.methodHelp': self.system_methodHelp,
            'system.multicall': self.system_multicall,
            }
        self.allow_none = allow_none
        self.encoding = encoding

    def register_function(self, function, name = None):
        """Registers a function to respond to XML-RPC requests.

        The optional name argument can be used to set a Unicode name
        for the function.
        """
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    @signature(list)
    def system_listMethods(self, request):
        """system.listMethods() => ['add', 'subtract', 'multiply']

        Returns a list of the methods supported by the server.
        """
        methods = self.funcs.keys()
        methods.sort()
        return methods

    @signature(list, str)
    def system_methodSignature(self, request, method_name):
        """system.methodSignature('add') => [['double', 'int', 'int']]

        Returns a list describing the possible signatures of the method.
        In the above example, the add method takes two integers as
        arguments and returns a double result.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        if hasattr(method, '_signature'):
            result = []
            for x in method._signature:
                if x is str:
                    result.append('string')
                else:
                    result.append(x.__name__)
            return [result]

    @signature(str, str)
    def system_methodHelp(self, request, method_name):
        """system.methodHelp('add') => "Adds two integers together"

        Returns a string containing documentation for the specified method.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        lines = method.__doc__.split('\n')
        lines = [line.strip() for line in lines]
        return '\n'.join(lines).strip()

    @signature(list, list)
    def system_multicall(self, request, call_list):
        """system.multicall([{'methodName': 'add', 'params': [2, 2]}]) => [[4]]

        Allows the caller to package multiple XML-RPC calls into a single
        request.

        See http://www.xmlrpc.com/discuss/msgReader$1208
        """
        results = []
        for call in call_list:
            method = call['methodName']
            params = call['params']
            result = self.dispatch(method, request, params)
            results.append([result])
        return results

    def dispatch(self, method, request, params):
        try:
            func = self.funcs[method]
        except KeyError:
            raise Exception('method "%s" is not supported' % method)
        response = func(request, *params)
        return (response, )

    def dispatch_and_marshal(self, method, request, params):
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
        params, method = xmlrpclib.loads(request.raw_post_data)
        return self.dispatch_and_marshal(method, request, params)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
