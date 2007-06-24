"""
Extract browser information from the User-Agent header.
"""

import os
import re


def get_engines():
    """
    Get all rendering engines from the database.

    Make sure that KHTML and Gecko are returned last, because some
    browsers include those names in their User-Agent string, in
    addition to their real engine name.
    """
    from shotserver04.browsers.models import Engine
    khtml = gecko = None
    for engine in Engine.objects.all():
        if engine.name == 'Gecko':
            gecko = engine
        elif engine.name == 'KHTML':
            khtml = engine
        else:
            yield engine
    if khtml:
        yield khtml
    if gecko:
        yield gecko


def get_browser_groups():
    """
    Get all browser groups from the database.

    Make sure that Firefox and Mozilla are returned last, because
    other browsers include those names in their User-Agent string.
    """
    from shotserver04.browsers.models import BrowserGroup
    firefox = mozilla = None
    for browser_group in BrowserGroup.objects.all():
        if browser_group.name == 'Firefox':
            firefox = browser_group
        elif browser_group.name == 'Mozilla':
            mozilla = browser_group
        else:
            yield browser_group
    if firefox:
        yield firefox
    if mozilla:
        yield mozilla


def extract_version(user_agent, name):
    """
    Extract version string that comes after the name.

    >>> extract_version('Mozilla/5.0', 'Mozilla')
    '5.0'
    >>> extract_version('Mozilla/5.0 Gecko/20061201 Firefox/2.0.0.4', 'Gecko')
    '20061201'
    >>> extract_version('Safari/417.8', 'Safari')
    '2.0.3'
    >>> extract_version('Version/3.0.2 Safari/522.13.1', 'Safari')
    '3.0.2'
    """
    if name == 'Safari' and 'Version' in user_agent:
       name = 'Version'
    index = user_agent.index(name)
    index += len(name)
    if user_agent[index] != '/':
        return ''
    index += 1
    start = index
    while index < len(user_agent) and user_agent[index] in '.0123456789':
        index += 1
    version = user_agent[start:index]
    if name == 'Safari':
       return safari_version(version)
    return version


def extract_major(version):
    """
    Extract major version number from version string.

    >>> extract_major('2.0.0.4')
    2
    >>> extract_major('2')
    2
    """
    if version.count('.'):
        return int(version.split('.')[0])
    elif version.isdigit():
        return int(version)


def extract_minor(version):
    """
    Extract minor version number from version string.

    >>> extract_minor('2.18')
    18
    >>> extract_minor('2.0.0.4')
    0
    """
    if version.count('.'):
        return int(version.split('.')[1])


uamatrix_findall = re.compile(r"""
<update.*?
<os_ver>10.*?
<safari_ver>(.+?)</safari_ver>.*?
<safari_bld>(.+?)</safari_bld>.*?
</update>
""", re.VERBOSE | re.DOTALL).findall


def safari_version(build):
   """
   Convert Safari build number to version number.

   >>> safari_version('419.3')
   '2.0.4'
   """
   module_dir = os.path.dirname(__file__)
   uamatrix_filename = os.path.join(module_dir, 'uamatrix.xml')
   uamatrix = open(uamatrix_filename).read()
   for safari_version, safari_build in uamatrix_findall(uamatrix):
      if safari_build == build:
         return safari_version
   return build


if __name__ == '__main__':
   import doctest
   doctest.testmod()
