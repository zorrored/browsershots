from django.conf import settings
from shotserver05.xmlrpc.utils import import_method
from shotserver05.system.utils import signature


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
    return [signature(method_name)]


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
