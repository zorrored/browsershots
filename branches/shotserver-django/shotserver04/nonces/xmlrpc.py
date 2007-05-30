from shotserver04.xmlrpc import signature
from shotserver04.nonces import crypto, util
from shotserver04.nonces.models import Nonce
from shotserver04.factories.models import Factory


@signature(str, str)
def challenge(request, factory_name):
    """
    Generate a nonce for authentication.

    The return value is a string that contains the password crypt
    algorithm (e.g. 'sha1'), the salt, and the nonce, separated by '$'
    signs::

      algo$salt$nonce
    """
    factory = Factory.objects.get(name=factory_name)
    hashkey = crypto.random_md5()
    ip = request.META['REMOTE_ADDR']
    Nonce.objects.create(factory=factory, hashkey=hashkey, ip=ip)
    password = factory.admin.password
    if password.count('$'):
        algo, salt, crypt = password.split('$')
    else:
        algo, salt, crypt = 'md5', '', password
    return '$'.join((algo, salt, hashkey))


@signature(str, str, str)
def checkPassword(request, factory_name, crypted_password):
    """
    Verify a crypted password that was created like this::

      md5(algo(salt + password) + nonce)

    The return value is the string 'OK' or a short error message.
    """
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    return util.verify(factory, ip, crypted_password)
