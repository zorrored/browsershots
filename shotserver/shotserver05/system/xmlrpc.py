from django.conf import settings
from shotserver05.xmlrpc.utils import import_method


def listMethods(request):
    """
    Get a list of the methods supported by the server.

    Return value:
    ~~~~~~~~~~~~~
    * method_names list (names of all supported methods)
    """
    result = []
    for full_app_name in settings.INSTALLED_APPS:
        package, app_name = full_app_name.split('.', 1)
        if package != 'shotserver05':
            continue
        module_name = full_app_name + '.xmlrpc'
        try:
            module = __import__(module_name)
        except ImportError:
            continue
        for part in module_name.split('.')[1:]:
            module = module.__dict__[part]
        for method_name in module.__dict__.keys():
            method = module.__dict__[method_name]
            if callable(method) and method.__module__ == module_name:
                result.append('.'.join((app_name, method_name)))
    result.sort()
    return result


def methodSignature(request, method_name):
    """
    List the possible signatures of the specified method.

    Arguments:
    ~~~~~~~~~~
    * method_name string (e.g. system.listMethods)

    Return value:
    ~~~~~~~~~~~~~
    * signatures list (usually only one signature)

    Each signature is a list of type name strings, first the type of
    the return value, then the types of the arguments.
    """
    method = import_method(method_name)
    lines = method.__doc__.splitlines()
    index = 0
    while index < len(lines) and lines[index].strip() != 'Arguments:':
        index += 1
    index += 1
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
    return [return_values + arguments]


def methodHelp(request, method_name):
    """
    Get documentation for the specified method.

    Arguments:
    ~~~~~~~~~~
    * method_name string (e.g. system.listMethods)

    Return value:
    ~~~~~~~~~~~~~
    * help string (method documentation)
    """
    method = import_method(method_name)
    if method.__doc__:
        return method.__doc__.strip().replace('\n    ', '\n')
    else:
        return "Sorry, no documentation is available for this method."
