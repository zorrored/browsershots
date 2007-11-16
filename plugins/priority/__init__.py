# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Priority processing for selected users or domains.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime
from shotserver04.priority.models import UserPriority, DomainPriority


def user_priority(user):
    """
    Get the best active priority for this user.
    """
    priorities = UserPriority.objects.filter(
        user=user, expire__gte=datetime.now())
    return max([0] + [p.priority for p in priorities])


def domain_priority(domain):
    """
    Get the best active priority for this domain name.
    """
    priorities = DomainPriority.objects.filter(
        domain=domain, expire__gte=datetime.now())
    return max([0] + [p.priority for p in priorities])
