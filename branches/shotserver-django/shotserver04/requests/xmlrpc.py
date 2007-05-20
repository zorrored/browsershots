from shotserver04.auth import util
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request


def poll(request, factory_name, crypted_password):
    """
    requests.poll('factory', 'crypt') => {'status': 'OK', 'request': 123}

    Find a matching screenshot request. If successful, the screenshot
    request is locked for the calling factory, and the function
    returns an array with information about the screenshot request.

    If an error occurs, the 'status' field in the result array will
    contain a short error message.
    """
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    status = util.verify(factory, ip, crypted_password)
    if status != 'OK':
        return {'status': status}
    matching_requests = Request.objects.filter(factory.features_q())
    if len(matching_requests) == 0:
        return {'status': 'No matching screenshot requests'}
    return {'status': 'OK'}
