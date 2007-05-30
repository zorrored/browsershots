from shotserver04.xmlrpc import signature
from shotserver04.nonces import util
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from datetime import datetime


@signature(dict, str, str)
def poll(request, factory_name, crypted_password):
    """
    Try to find a matching screenshot request for a given factory.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)
    * crypted string (lowercase hexadecimal, length 32)

    Return value
    ~~~~~~~~~~~~
    * options dict (screenshot request configuration)

    If successful, the options dict will have the following keys:

    * status string ('OK' or short error message)
    * browser string (browser name)
    * version string (browser version)
    * width int (screen width in pixels)
    * height int (screen height in pixels)
    * bpp int (color depth in bits per pixel)
    * javascript string (javascript version)
    * java string (java version)
    * flash string (flash version)
    * command string (browser command to run)

    The matching screenshot request is locked for 3 minutes. This is
    to make sure that no requests are processed by two factories at
    the same time. If your factory takes longer to process a request,
    it is possible that somebody else will lock it. In this case, your
    upload will fail.

    If an error occurs, the 'status' field in the result dict will
    contain a short error message, and the other keys will not be
    available.
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
