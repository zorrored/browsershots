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
Display ads on the site, if configured in settings.py.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def ads_leaderboard():
    """
    Display a leaderboard ad, if configured in settings.py.
    """
    if not hasattr(settings, 'ADS_LEADERBOARD'):
        return ''
    return settings.ADS_LEADERBOARD.strip()


@register.simple_tag
def ads_skyscraper():
    """
    Display a skyscraper ad, if configured in settings.py.
    """
    if not hasattr(settings, 'ADS_SKYSCRAPER'):
        return ''
    return settings.ADS_SKYSCRAPER.strip()
