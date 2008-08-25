from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from shotserver05.xmlrpc.utils import user_auth, factory_auth
from shotserver05.factories.models import Factory
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.utils import last_poll_timeout


##################### Methods for authenticated user #########################


@user_auth
def createFactory(request, user, factory_name, operating_system, hardware):
    """
    Create a new screenshot factory.

    Arguments:
    ~~~~~~~~~~
    * username string (regular Django user account)
    * factory_name string (lowercase, use hostname if possible)
    * operating_system string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    operating_system = get_object_or_404(
        OperatingSystem, slug=operating_system)
    Factory.objects.create(name=factory_name, user=user,
        operating_system=operating_system, hardware=hardware)
    return 'OK'


@user_auth
def updateFactory(request, user, factory_name, operating_system, hardware):
    """
    Update factory information.

    Arguments:
    ~~~~~~~~~~
    * username string (e.g. joe)
    * factory_name string (lowercase)
    * operating_system string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    factory = get_object_or_404(Factory, name=factory_name)
    if factory.user != user:
        raise xmlrpclib.Fault(401, "Unauthorized.")
    operating_system = get_object_or_404(
        OperatingSystem, slug=operating_system)
    factory.update_fields(
        operating_system = operating_system,
        hardware = hardware)
    return 'OK'


#################### Methods for authenticated factory #######################


@factory_auth
def testAuth(request, factory, dummy_number, dummy_text):
    """
    Test factory authentication with MD5 hash. To compute the hash,
    concatenate the string values of all the other arguments and the
    secret key for the factory, then get the MD5 hash as 32 lowercase
    hexadecimal characters. If the factory name is 'factory' and the
    secret key is 'secret', you might get the following MD5 hash:

    >>> md5('123hello2008-08-08T23:56:14Zfactorysecret').hexdigest()
    '5afba7f48c2df4b85e3cac482df48010'

    Arguments:
    ~~~~~~~~~~
    * factory_name string (lowercase)
    * dummy_number int (e.g. 123)
    * dummy_text string (e.g. hello)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    return 'OK'


###################### Methods without authentication ########################


def listActive(request):
    """
    List all screenshot factories that are currently active.

    Return value:
    ~~~~~~~~~~~~~
    * factories list
    """
    factories = Factory.objects.filter(last_poll__gte=last_poll_timeout())
    return [factory.name for factory in factories]


def details(request, factory_name):
    """
    Get details for the specified screenshot factory.

    Arguments:
    ~~~~~~~~~~
    * factory_name string (lowercase)

    Return value:
    ~~~~~~~~~~~~~
    * details dict

    The return dict will contain the following entries:

    * name string (lowercase)
    * operating_system string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)
    * last_poll string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * last_upload string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * last_error string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    """
    factory = get_object_or_404(Factory, name=factory_name)
    return {
        'name': factory.name,
        'operating_system': factory.operating_system.slug,
        'hardware': factory.hardware,
        'last_poll': factory.last_poll or '',
        'last_upload': factory.last_upload or '',
        'last_error': factory.last_error or '',
        }
