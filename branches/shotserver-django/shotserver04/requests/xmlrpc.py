from xmlrpclib import Fault
from django.db.models import Q
from shotserver04.common import serializable, get_or_fault
from shotserver04.xmlrpc import register
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.requests.models import Request
from datetime import datetime, timedelta


@serializable
def find_and_lock_request(factory, features):
    # Find matching request
    five_minutes_ago = datetime.now() - timedelta(0, 300)
    matches = Request.objects.select_related()
    matches = matches.filter(features)
    matches = matches.filter(uploaded__isnull=True)
    matches = matches.filter(
        Q(locked__isnull=True) | Q(locked__lt=five_minutes_ago))
    matches = matches.order_by(
        '-requests_request__request_group.submitted')
    matches = matches[:1]
    if len(matches) == 0:
        raise Fault(0, 'No matching request.')
    request = matches[0]
    # Lock request
    request.factory = factory
    request.locked = datetime.now()
    request.save()
    return request


@register(dict, str, str)
def poll(http_request, factory_name, encrypted_password):
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
    * request int (for redirect and screenshots.upload)
    * command string (browser command to run)
    * browser string (browser name)
    * version string (browser version)
    * width int (screen width in pixels)
    * height int (screen height in pixels)
    * bpp int (color depth in bits per pixel)
    * javascript string (javascript version)
    * java string (java version)
    * flash string (flash version)

    If an error occurs, the 'status' field in the result dict will
    contain a short error message, and the other keys will not be
    available.

    Locking
    ~~~~~~~
    The matching screenshot request is locked for five minutes. This
    is to make sure that no requests are processed by two factories at
    the same time. If your factory takes longer to process a request,
    it is possible that somebody else will lock it. In this case, your
    upload will fail.
    """
    # Verify authentication
    factory = get_or_fault(Factory, name=factory_name)
    nonces.verify(http_request, factory, encrypted_password)
    # Update last_poll timestamp
    factory.last_poll = datetime.now()
    factory.save()
    # Get matching request
    request = find_and_lock_request(factory, factory.features_q())
    # Get matching browser
    try:
        browser = Browser.objects.select_related().get(
            factory=factory,
            browser_group=request.browser_group,
            major=request.major,
            minor=request.minor)
    except Browser.DoesNotExist:
        raise Fault(0, "No matching browser for selected request.")
    command = browser.command
    if not command:
        command = browser.browser_group.name.lower()
    # Build result dict
    return {
        'request': request.id,
        'command': command,
        'browser': browser.browser_group.name,
        'version': browser.version,
        'width': request.request_group.width or 0,
        'height': request.request_group.height or 0,
        'bpp': request.request_group.bits_per_pixel or 0,
        'javascript': request.request_group.javascript,
        'java': request.request_group.java,
        'flash': request.request_group.flash,
        }
