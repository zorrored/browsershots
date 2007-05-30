from shotserver04.xmlrpc import signature
from shotserver04.nonces import crypto, util
from shotserver04.nonces.models import Nonce
from shotserver04.factories.models import Factory


@signature(str, str)
def challenge(request, factory_name):
    """
    Generate a nonce for authentication.

    Arguments:
        factory_name string (lowercase, normally from hostname)

    Return value:
        challenge string (algorithm$salt$nonce)

    The return value is a string that contains the password crypt
    algorithm (sha1 or md5), the salt, and the nonce, separated by '$'
    signs, for example::

        sha1$Y7JaR/..$eb403b48ec9bf887ba645408acad17a5
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
def verify(request, factory_name, crypted_password):
    """
    Test authentication with a crypted password.

    Arguments:
        factory_name string (lowercase, normally from hostname)
        crypted_password string (lowercase hexadecimal, length 32)

    Return value:
        status string ('OK' or short error message)

    To compute the crypted password, you must first generate a nonce
    and get the crypt algorithm and salt (see nonces.challenge). Then
    you can encrypt the password like this::

        crypted_password = md5(sha1(salt + password) + nonce)

    If requested by the challenge, you must use md5 rather than sha1
    for the inner hash. The result of each hash function call must be
    formatted as lowercase hexadecimal. The calls to nonces.challenge
    and nonces.verify must be made from the same IP address.
    """
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    return util.verify(factory, ip, crypted_password)
