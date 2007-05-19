# Inspired by SimpleXMLRPCServer.py by Brian Quinlan (brian@sweetapp.com).

import re
import sys
import xmlrpclib

signature_match = re.compile(r'^([\w\.]+)\((.*?)\)\s*=>\s*(.*)$').match


def first_parameter(values):
    if values.startswith('['):
        types, rest = parse_types(values[1:])
        assert rest.startswith(']')
        return 'array', rest[1:]
    elif values.startswith('('):
        types, rest = parse_types(values[1:])
        assert rest.startswith(')')
        return 'tuple', rest[1:]
    elif values.startswith('{'):
        types, rest = parse_types(values[1:], ',:')
        assert rest.startswith('}')
        return 'dict', rest[1:]
    elif values.startswith('"'):
        index = 1
        while index < len(values) and (
            values[index] != '"' or values[index-1] == '\\'):
            index += 1
        return 'string', values[index+1:]
    elif values.startswith("'"):
        index = 1
        while index < len(values) and (
            values[index] != "'" or values[index-1] == '\\'):
            index += 1
        return 'string', values[index+1:]
    elif values[0] in '0123456789':
        index = 1
        while index < len(values) and values[index] in '0123456789.':
            index += 1
        if values[:index].count('.'):
            return 'float', values[index:]
        else:
            return 'int', values[index:]
    words = values.split(',')
    first_word = words[0].strip()
    if first_word in ('True', 'False'):
        return 'bool', values[len(words[0]):]
    return 'unknown', values


def parse_types(values, separators=','):
    """
    >>> parse_types('[], (), {}, "", 1')
    (['array', 'tuple', 'dict', 'string', 'int'], '')
    >>> parse_types("['(']")
    (['array'], '')
    >>> parse_types('{1:["a"]}')
    (['dict'], '')
    """
    if values.strip() == '':
        return [], ''
    types = []
    while values:
        type_name, values = first_parameter(values)
        types.append(type_name)
        values = values.lstrip()
        if values and values[0] in separators:
            values = values[1:].lstrip()
        else:
            return types, values


class Dispatcher:

    def __init__(self, allow_none=False, encoding=None):
        self.funcs = {
            'system.listMethods' : self.system_listMethods,
            'system.methodSignature' : self.system_methodSignature,
            'system.methodHelp' : self.system_methodHelp,
            'system.multicall' : self.system_multicall,
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

    def system_listMethods(self, request):
        """system.listMethods() => ['add', 'subtract', 'multiply']

        Returns a list of the methods supported by the server.
        """
        methods = self.funcs.keys()
        methods.sort()
        return methods

    def system_methodSignature(self, request, method_name):
        """system.methodSignature('add') => [['double', 'int', 'int']]

        Returns a list describing the possible signatures of the method.
        In the above example, the add method takes two integers as
        arguments and returns a double result.
        """
        if not self.funcs.has_key(method_name):
            return 'method not found'
        method = self.funcs[method_name]
        lines = method.__doc__.split('\n')
        while lines and lines[0].strip() == '':
            lines.pop(0)
        if not lines:
            return 'empty docstring'
        first_line = lines[0].strip()
        match = signature_match(first_line)
        if not match:
            return 'signature not found'
        name, params, result = match.groups()
        if name != method_name:
            return 'signature name mismatch'
        result_types, rest = parse_types(result)
        params_types, rest = parse_types(params)
        return [result_types + params_types]

    def system_methodHelp(self, request, method_name):
        """system.methodHelp('add') => "Adds two integers together"

        Returns a string containing documentation for the specified method.
        """
        if not self.funcs.has_key(method_name):
            return 'method not found'
        method = self.funcs[method_name]
        return method.__doc__

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
        response = (response, )

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
