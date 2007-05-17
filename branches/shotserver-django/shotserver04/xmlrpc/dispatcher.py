import re
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

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


class SignatureDispatcher(SimpleXMLRPCDispatcher):

    def system_methodSignature(self, method_name):
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
