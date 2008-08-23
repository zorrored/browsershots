from django.conf import settings
from shotserver05.xmlrpc.utils import signature, import_method


@signature(list)
def listMethods(request):
    """
    Get a list of the methods supported by the server.
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
            if hasattr(method, '_signature'):
                result.append('.'.join((app_name, method_name)))
    result.sort()
    return result


@signature(list, str)
def methodSignature(request, method_name):
    """
    Get a list describing the possible signatures of the method.
    """
    method = import_method(method_name)
    result = []
    for type in method._signature:
        name = type.__name__
        if name == 'str':
            name = 'string'
        result.append(name)
    return [result]


@signature(str, str)
def methodHelp(request, method_name):
    """
    Get a string containing documentation for the specified method.
    """
    method = import_method(method_name)
    if method.__doc__:
        return method.__doc__.strip().replace('\n    ', '\n')
    else:
        return ''
