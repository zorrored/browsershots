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
Utility functions for revenue sharing.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime
from shotserver04.priority.models import UserPriority


def month_revenue(year, month):
    """
    Get the total monthly shared revenue, in Euros.
    """
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
    priorities = UserPriority.objects.filter(
        activated__gte=datetime(year, month, 1),
        activated__lt=datetime(next_year, next_month, 1))
    euros = sum([p.payment for p in priorities.filter(currency='EUR')])
    dollars = sum([p.payment for p in priorities.filter(currency='USD')])
    return (float(euros) + (float(dollars) / 1.5)) / 2
