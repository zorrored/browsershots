from shotserver04.auth.models import Nonce
from shotserver04.factories.models import Factory
from shotserver04.auth import crypto, util


def challenge(request, factory_name):
    """
    auth.challenge('factory') => ['nonce0123456789abcdef', 'sha1', 'salt123']
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
    return hashkey, algo, salt


def test(request, factory_name, crypted_password):
    """
    auth.test('factory', 'crypt') => 'OK'
    """
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    return util.verify(factory, ip, crypted_password)
