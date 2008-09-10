# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
XML-RPC methods for the platforms app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

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
