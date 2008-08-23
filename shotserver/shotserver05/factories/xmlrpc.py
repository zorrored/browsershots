from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from shotserver05.xmlrpc.utils import signature, user_auth, factory_auth
from shotserver05.factories.models import Factory
from shotserver05.factories.utils import last_poll_timeout


@signature(list)
def active(request):
    """
    List active screenshot factories.
    """
    factories = Factory.objects.filter(last_poll__gte=last_poll_timeout())
    return [factory.name for factory in factories]


@signature(dict, str)
def details(request, factory_name):
    """
    Get details for the specified screenshot factory.
    """
    factory = get_object_or_404(Factory, name=factory_name)
    result = {}
    for key, value in factory.__dict__.iteritems():
        if 'secret' in key:
            continue
        if value is None or isinstance(value, datetime):
            value = value.astimezone(None).isoformat()
        result[key] = value
    return result


##################### Methods for authenticated user #########################


@user_auth
@signature(str, str, str)
def create(request, user, factory_name, operating_system_slug, hardware):
    """
    Create a new screenshot factory.

    * factory_name string
    * operating_system_slug string
    * hardware string
    """
    operating_system = get_object_or_404(
        OperatingSystem, slug=operating_system_slug)
    Factory.objects.create(name=name, user=user,
        operating_system=operating_system, hardware=hardware)
    return 'OK'


#################### Methods for authenticated factory #######################


@factory_auth
@signature(str, int, str)
def testAuth(request, factory, dummy_number, dummy_text):
    """
    Test factory authentication with MD5 hash. To compute the hash,
    concatenate the string values of all the other arguments and the
    secret key for the factory, then get the MD5 hash as 32 lowercase
    hexadecimal characters.

    * dummy_number int (for example, 123)
    * dummy_text string (for example, hello)

    If the factory name is 'factory' and the secret key is 'secret',
    you might get the following MD5 hash:

    >>> md5('123hello2008-08-08T23:56:14Zfactorysecret').hexdigest()
    '5afba7f48c2df4b85e3cac482df48010'
    """
    return 'OK'


@factory_auth
@signature(str, str, str, str)
def update(request, factory, operating_system_slug, hardware):
    """
    Update factory information.

    * operating_system_slug string
    * hardware string
    """
    factory.update_fields(operating_system=operating_system,
                          hardware=hardware)
    return 'OK'
