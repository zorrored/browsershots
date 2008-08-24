import time
from datetime import datetime, timedelta
import xmlrpclib
from django.conf import settings
from django.contrib.auth.models import User
from shotserver05.factories.models import Factory

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


def update_docstring(wrapper, insert):
    lines = wrapper.__doc__.splitlines()
    index = 0
    while not lines[index].lstrip().startswith('*'):
        index += 1
    while lines[index].lstrip().startswith('*'):
        index += 1
    lines[index:index] = insert
    wrapper.__doc__ = '\n'.join(lines)


def check_hash(func_name, args, secret, submitted_hash):
    """
    Check the MD5 hash of all arguments.
    """
    message = ' '.join([func_name] + [str(arg) for arg in args] + [secret])
    correct_hash = md5(message).hexdigest()
    # print message, correct_hash
    if submitted_hash != correct_hash:
        raise xmlrpclib.Fault(401,
            "Authentication failed: incorrect MD5 hash.")


def check_timestamp(timestamp):
    """
    Check the submitted timestamp.
    """
    time_tuple = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")[:6]
    submitted = datetime(*time_tuple)
    now = datetime.utcnow()
    offset = abs(now - submitted)
    # print submitted, now, str(offset)
    if offset > timedelta(minutes=5):
        raise xmlrpclib.Fault(401,
            "Authentication failed: timestamp offset is %s." % offset)


def user_auth(func):
    """
    Decorator for user authentication with MD5 hash. The following
    additional arguments are required:

    * timestamp string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * md5_hash string (see users.testAuth for details)
    """

    def wrapper(*args):
        request, username = args[:2]
        timestamp, submitted_hash = args[-2:]
        # print 'username', username
        # print 'timestamp', timestamp
        # print 'hash', submitted_hash
        user = User.objects.get(username=username)
        app_name = func.__module__.split('.')[-2]
        func_name = '.'.join((app_name, func.__name__))
        check_hash(func_name, args[1:-1], user.password, submitted_hash)
        check_timestamp(timestamp)
        return func(request, user, *args[2:-2])

    update_wrapper(wrapper, func)
    lines = user_auth.__doc__.splitlines()
    insert = [l for l in lines if l.lstrip().startswith('*')]
    if func.__name__ == 'testAuth':
        insert[-1] = insert[-1].replace('users.testAuth', 'below')
    update_docstring(wrapper, insert)
    return wrapper


def factory_auth(func):
    """
    Decorator for factory authentication with MD5 hash. The following
    additional arguments are required:

    * timestamp string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * md5_hash string (see factories.testAuth for details)
    """

    def wrapper(*args):
        request, factory_name = args[:2]
        timestamp, submitted_hash = args[-2:]
        # print 'factory_name', factory_name
        # print 'timestamp', timestamp
        # print 'hash', submitted_hash
        factory = Factory.objects.get(name=factory_name)
        app_name = func.__module__.split('.')[-2]
        func_name = '.'.join((app_name, func.__name__))
        check_hash(func_name, args[1:-1], factory.secret_key, submitted_hash)
        check_timestamp(timestamp)
        return func(request, factory, *args[2:-2])

    update_wrapper(wrapper, func)
    lines = factory_auth.__doc__.splitlines()
    insert = [l for l in lines if l.lstrip().startswith('*')]
    if func.__name__ == 'testAuth':
        insert[-1] = insert[-1].replace('factories.testAuth', 'below')
    update_docstring(wrapper, insert)
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
