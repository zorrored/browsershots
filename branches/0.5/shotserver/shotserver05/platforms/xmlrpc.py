from django.shortcuts import get_object_or_404
from shotserver05.platforms.models import OperatingSystem


def listOperatingSystems(request):
    """
    List all available operating systems.

    Return value:
    ~~~~~~~~~~~~~
    * slugs list (a slug for each operating system)
    """
    return [os.slug for os in OperatingSystem.objects.all()]


def operatingSystemDetails(request, operating_system):
    """
    Get details for the specified operating system.

    Arguments:
    ~~~~~~~~~~
    * operating_system string (see platforms.listOperatingSystems)

    Return value:
    ~~~~~~~~~~~~~
    * details dict

    The result dict will contain the following entries:

    * platform string
    * name string
    * version string
    * codename string
    """
    os = get_object_or_404(OperatingSystem, slug=operating_system)
    return {
        'platform': os.platform.name,
        'name': os.name,
        'version': os.version,
        'codename': os.codename,
        }
