# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Show a table with SQL queries for the current HTTP request, for
debugging and optimizing.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import template
from django.utils.text import capfirst
from shotserver04 import settings

register = template.Library()


@register.simple_tag
def hosting_provider():
    """
    Display an HTML link to the hosting provider.
    """
    if (not hasattr(settings, 'HOSTING_PROVIDER') or
        not settings.HOSTING_PROVIDER or
        not hasattr(settings, 'HOSTING_PROVIDER_URL') or
        not settings.HOSTING_PROVIDER_URL):
        return ''
    link = '<a href="%s">%s</a>' % (settings.HOSTING_PROVIDER_URL,
                                    settings.HOSTING_PROVIDER)
    return '| ' + capfirst(_("hosted by %(provider)s")) % {'provider': link}
