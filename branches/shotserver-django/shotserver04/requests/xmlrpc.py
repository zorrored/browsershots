from shotserver04.xmlrpc import signature
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from shotserver04.browsers.models import Browser
from datetime import datetime


@signature(dict, str, str)
def poll(request, factory_name, encrypted_password):
    """
    Try to find a matching screenshot request for a given factory.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)
    * encrypted_password string (lowercase hexadecimal, length 32)

    See nonces.verify for how to encrypt your password.

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

    If an error occurs, the 'status' field in the result dict will
    contain a short error message, and the other keys will not be
    available.

    Locking
    ~~~~~~~
    The matching screenshot request is locked for 3 minutes. This is
    to make sure that no requests are processed by two factories at
    the same time. If your factory takes longer to process a request,
    it is possible that somebody else will lock it. In this case, your
    upload will fail.
    """
    # Verify authentication
    factory = Factory.objects.get(name=factory_name)
    status = nonces.verify(request, factory, encrypted_password)
    if status != 'OK':
        return {'status': status}
    # Update last_poll timestamp
    factory.last_poll = datetime.now()
    factory.save()
    # Find matching request
    matches = Request.objects.select_related()
    matches = matches.filter(factory.features_q())
    matches = matches.order_by('-requests_request__request_group.submitted')
    matches = matches[:1]
    if len(matches) == 0:
        return {'status': 'No matching screenshot requests'}
    request = matches[0]
    browser = Browser.objects.select_related().get(
        factory=factory,
        browser_group=request.browser_group,
        major=request.major,
        minor=request.minor)
    return {
        'status': 'OK',
        'browser': browser.browser_group.name,
        'command': browser.command,
        'width': request.request_group.width,
        'bpp': request.request_group.bits_per_pixel,
        }
