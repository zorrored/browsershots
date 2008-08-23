from shotserver05.platforms.models import OperatingSystem


def listOperatingSystems(request):
    """
    List all available operating systems.

    Return value:
    ~~~~~~~~~~~~~
    * slugs list (a slug for each operating system)
    """
    return [os.slug for os in OperatingSystem.objects.all()]
