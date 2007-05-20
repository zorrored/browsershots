from shotserver04.auth import util


def poll(request, factory_name, crypted_password):
    """
    requests.poll('factory', 'crypt') => {'status': 'OK', 'request': 123}
    """
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    status = util.verify(factory, ip, crypted_password)
    if status != 'OK':
        return {'status': status}
    return {'status': 'OK'}
