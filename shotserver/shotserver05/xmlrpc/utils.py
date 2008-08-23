import xmlrpclib
from django.conf import settings

try:
    from hashlib import md5
except ImportError:
    from md5 import md5

try:
    from functools import update_wrapper
except ImportError: # using Python version < 2.5
    def update_wrapper(wrapper, wrapped):
        wrapper.__name__ = wrapped.__name__
        wrapper.__module__ = wrapped.__module__
        wrapper.__doc__ = wrapped.__doc__
        wrapper.__dict__.update(wrapped.__dict__)
        return wrapper


def update_docstring(wrapper, insert, append):
    lines = wrapper.__doc__.splitlines()
    index = 0
    while not lines[index].lstrip().startswith('*'): index += 1
    while lines[index].lstrip().startswith('*'): index += 1
    lines = lines[:index] + insert + lines[index:] + append
    wrapper.__doc__ = '\n'.join(lines)


def signature(*types):
    """
    Decorator to add a signature to a function or method.
    """

    def save(func):
        """Save the signature."""
        func._signature = types
        return func

    return save


def check_hash(args, name, secret, submitted_hash):
    """
    Check the MD5 hash of all arguments.
    """
    hash = md5()
    for arg in args:
        hash.update(str(arg))
    hash.update(name)
    hash.update(secret)
    correct_hash = hash.hexdigest()
    if submitted_hash != correct_hash:
        raise xmlrpclib.Fault(401,
            "Authentication failed: incorrect MD5 hash.")


def check_timestamp(timestamp):
    """
    Check the submitted timestamp.
    """
    time_tuple = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")[:6]
    offset = abs(datetime.utcnow() - datetime(*time_tuple))
    print str(offset)
    if offset > timedelta(minutes=5):
        raise xmlrpclib.Fault(401,
            "Authentication failed: timestamp offset is %s." % offset)


def user_auth(func):
    """
    Decorator for user authentication with MD5 hash. The following
    additional arguments are required:

    * timestamp string (ISO 8601 UTC: YYYY-MM-DDThh:mm:ssZ)
    * username string (regular Django user account)
    * md5_hash string (32 lowercase hexadecimal characters)

    See users.testAuth for how to compute md5_hash.
    """

    def wrapper(*args):
        submitted_hash = args.pop(-1)
        username = args.pop(-1)
        user = User.objects.get(username=username)
        check_hash(args, username, user.password, submitted_hash)
        timestamp = args.pop(-1)
        check_timestamp(timestamp)
        return func(user, *args)

    update_wrapper(wrapper, func)
    lines = user_auth.__doc__.splitlines()
    insert = [l for l in lines if l.lstrip().startswith('*')]
    append = [l for l in lines if func.__name__ != 'testAuth' in l]
    update_docstring(wrapper, insert, append)
    wrapper._signature = func._signature + (str, str, str)
    return wrapper


def factory_auth(func):
    """
    Decorator for factory authentication with MD5 hash. The following
    additional arguments are required:

    * timestamp string (ISO 8601 UTC: YYYY-MM-DDThh:mm:ssZ)
    * factory_name string (screenshot factory name)
    * md5_hash string (32 lowercase hexadecimal characters)

    See factories.testAuth for how to compute md5_hash.
    """

    def wrapper(*args):
        submitted_hash = args.pop(-1)
        factory_name = args.pop(-1)
        factory = Factory.objects.get(name=factory_name)
        check_hash(args, factory_name, factory.secret_key, submitted_hash)
        timestamp = args.pop(-1)
        check_timestamp(timestamp)
        return func(factory, *args)

    update_wrapper(wrapper, func)
    lines = factory_auth.__doc__.splitlines()
    insert = [l for l in lines if l.lstrip().startswith('*')]
    append = [l for l in lines if func.__name__ != 'testAuth' in l]
    update_docstring(wrapper, insert, append)
    wrapper._signature = func._signature + (str, str, str)
    return wrapper


def import_method(app_method):
    """
    Import an XML-RPC method by name.
    """
    if app_method.count('.') != 1:
        raise xmlrpclib.Fault(404, "Method not found: " + app_method)
    app, method = app_method.split('.')
    if 'shotserver05.' + app not in settings.INSTALLED_APPS:
        raise xmlrpclib.Fault(404, "App not found: " + app)
    if method.startswith('_'):
        raise xmlrpclib.Fault(403, "This method is private: " + app_method)
    mod_name = 'shotserver05.%s.xmlrpc' % app
    try:
        mod = __import__(mod_name)
    except ImportError, error:
        raise xmlrpclib.Fault(404, "Module not found: " + str(error))
    mod = mod.__dict__[app].xmlrpc
    if method not in mod.__dict__:
        raise xmlrpclib.Fault(404, "Method not found: " + app_method)
    return mod.__dict__[method]
