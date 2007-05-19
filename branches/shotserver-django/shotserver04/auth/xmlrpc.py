from shotserver04.auth.models import Nonce
from shotserver04.factories.models import Factory
from shotserver04.auth import crypto


def challenge(request, factory_name):
    """
    auth.challenge('factory') => ['nonce0123456789abcdef', 'sha1', 'salt123']
    """
    factory = Factory.objects.filter(name=factory_name)[0]
    hashkey = crypto.random_md5()
    ip = request.META['REMOTE_ADDR']
    Nonce.objects.create(factory=factory, hashkey=hashkey, ip=ip)
    password = factory.admin.password
    if password.count('$'):
        algo, salt, crypt = password.split('$')
    else:
        algo, salt, crypt = 'md5', '', password
    return hashkey, algo, salt


def test(request, factory_name, attempt):
    """
    auth.test('factory', 'crypt0123456789abcdef') => 'OK'
    """
    factory = Factory.objects.filter(name=factory_name)[0]
    ip = request.META['REMOTE_ADDR']
    password = factory.admin.password
    if password.count('$'):
        algo, salt, crypt = password.split('$')
    else:
        algo, salt, crypt = 'md5', '', password
    matches = Nonce.objects.filter(ip=ip).extra(
        where=["MD5('%s' || hashkey) = '%s'" % (crypt, attempt)])
    if len(matches) == 0:
        return 'Password mismatch'
    elif len(matches) > 1:
        return 'Crypt hash collision'
    matches[0].delete()
    return 'OK'
