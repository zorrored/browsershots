from shotserver04.auth.models import Nonce
from datetime import datetime, timedelta


def verify(factory, ip, input):
    password = factory.admin.password
    if password.count('$'):
        algo, salt, crypt = password.split('$')
    else:
        algo, salt, crypt = 'md5', '', password
    nonces = Nonce.objects.filter(factory=factory, ip=ip).extra(
        where=["MD5(%s || hashkey) = %s"], params=[crypt, input])
    if len(nonces) == 0:
        return 'Password mismatch'
    if len(nonces) > 1:
        return 'Hash collision'
    nonce = nonces[0]
    if datetime.now() - nonce.created > timedelta(0, 600, 0):
        return 'Nonce expired'
    nonce.delete()
    return 'OK'
