from shotserver04.xmlrpc import signature
from shotserver04.nonces import util
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from datetime import datetime


@signature(dict, str, str)
def poll(request, factory_name, crypted_password):
    """
    Find a matching screenshot request. If successful, the screenshot
    request is locked for the calling factory, and the function
    returns a dict with information about the screenshot request.

    If an error occurs, the 'status' field in the result dict will
    contain a short error message.
    """
    # Verify authentication
    factory = Factory.objects.get(name=factory_name)
    ip = request.META['REMOTE_ADDR']
    status = util.verify(factory, ip, crypted_password)
    if status != 'OK':
        return {'status': status}

    # Update last_poll timestamp
    factory.last_poll = datetime.now()
    factory.save()

    # Find matching request
    matching_requests = Request.objects.filter(factory.features_q())
    if len(matching_requests) == 0:
        return {'status': 'No matching screenshot requests'}
    return {'status': 'OK'}
