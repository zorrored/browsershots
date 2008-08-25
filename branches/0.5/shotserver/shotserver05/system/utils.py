from shotserver05.xmlrpc.utils import import_method


def signature(method_name):
    method = import_method(method_name)
    lines = method.__doc__.splitlines()
    index = 0
    while index < len(lines) and lines[index].strip() != 'Arguments:':
        index += 1
    index += 1
    if index < len(lines):
        assert lines[index].strip() == '~~~~~~~~~~'
    index += 1
    arguments = []
    while index < len(lines) and lines[index].strip().startswith('*'):
        arguments.append(lines[index].split()[2])
        index += 1
    if index >= len(lines):
        index = 0
    while index < len(lines) and lines[index].strip() != 'Return value:':
        index += 1
    index += 1
    if index < len(lines):
        assert lines[index].strip() == '~~~~~~~~~~~~~'
    index += 1
    return_values = []
    while index < len(lines) and lines[index].strip().startswith('*'):
        return_values.append(lines[index].split()[2])
        index += 1
    if len(return_values) < 1:
        return_values = ['string']
    if len(return_values) > 1:
        return_values = ['list']
    return return_values + arguments
