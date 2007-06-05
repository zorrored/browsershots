import xmlrpclib
from shotserver04.xmlrpc import signature, ErrorMessage
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request
from shotserver04.screenshots.models import Screenshot
from shotserver04.screenshots import storage


@signature(str, str, str, int, xmlrpclib.Binary)
def upload(http_request,
           factory_name, encrypted_password, request, screenshot):
    """
    Submit a multi-page screenshot as a lossless PNG file.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)
    * encrypted_password string (lowercase hexadecimal, length 32)
    * request int (from requests.poll)
    * screenshot binary (BASE64-encoded PNG file)

    See nonces.verify for how to encrypt your password.

    Return value
    ~~~~~~~~~~~~
    * status string ('OK' or short error message)
    """
    # Verify authentication
    factory = Factory.objects.get(name=factory_name)
    nonces.verify(http_request, factory, encrypted_password)
    try:
        request_id = request
        request = Request.objects.get(pk=request_id)
    except Request.DoesNotExist:
        raise ErrorMessage("Request %d not found." % request_id)
    # Make sure the request was locked by this factory
    request.check_factory_lock(factory)
    # Make sure the request was redirected by the browser
    browser = request.browser
    if browser is None:
        raise ErrorMessage(
            "The browser has not visited the requested website.")
    # Store and check screenshot file
    hashkey = storage.save_upload(screenshot)
    ppmname = storage.pngtoppm(hashkey)
    magic, width, height = storage.read_pnm_header(ppmname)
    # Save screenshot in database
    screenshot = Screenshot(
        factory=factory, browser=browser, request=request,
        hashkey=hashkey, width=width, height=height)
    screenshot.save()
    return 'OK'
