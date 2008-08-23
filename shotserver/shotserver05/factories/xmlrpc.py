from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from shotserver05.xmlrpc.utils import user_auth, factory_auth
from shotserver05.factories.models import Factory
from shotserver05.factories.utils import last_poll_timeout


def active(request):
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

    * factory_name string (lowercase)
    * operating_system_slug string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)
    * last_poll string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * last_upload string (UTC, ISO 8601: YYYY-MM-DDThh:mm:ssZ)
    * uploads_per_hour int (in the last 60 minutes)
    * uploads_per_day int (in the last 24 hours)
    * errors_per_hour int (in the last 60 minutes)
    * errors_per_day int (in the last 24 hours)
    * problems_per_day int (in the last 24 hours)
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
def create(request, user, factory_name, operating_system_slug, hardware):
    """
    Create a new screenshot factory.

    Arguments:
    ~~~~~~~~~~
    * factory_name string (lowercase, use hostname if possible)
    * operating_system_slug string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    operating_system = get_object_or_404(
        OperatingSystem, slug=operating_system_slug)
    Factory.objects.create(name=name, user=user,
        operating_system=operating_system, hardware=hardware)
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
    * dummy_number int (e.g. 123)
    * dummy_text string (e.g. hello)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    return 'OK'


@factory_auth
def update(request, factory, operating_system_slug, hardware):
    """
    Update factory information.

    Arguments:
    ~~~~~~~~~~
    * operating_system_slug string (see platforms.listOperatingSystems)
    * hardware string (e.g. MacBook, Intel Core Duo, 2 GHz, 2 GB)

    Return value:
    ~~~~~~~~~~~~~
    * status string (OK)
    """
    factory.update_fields(operating_system=operating_system,
                          hardware=hardware)
    return 'OK'
