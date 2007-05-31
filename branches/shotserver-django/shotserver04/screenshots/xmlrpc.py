import xmlrpclib
from shotserver04.xmlrpc import signature
from shotserver04.nonces import xmlrpc as nonces
from shotserver04.factories.models import Factory


@signature(str, str, str, int, xmlrpclib.Binary)
def upload(post, factory_name, encrypted_password, request, screenshot):
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
    status = nonces.verify(post, factory, encrypted_password)
    if status != 'OK':
        return status
    return 'OK'
