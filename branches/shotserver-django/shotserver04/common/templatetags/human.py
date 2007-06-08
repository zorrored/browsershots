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
Convert times to a short human-readable format.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime
from django import template

register = template.Library()


@register.filter
def human_seconds(seconds):
    if seconds < 180:
        return "%d s" % seconds
    minutes = seconds / 60
    if minutes < 180:
        return "%d min" % minutes
    hours = minutes / 60
    if hours < 72:
        return "%d h" % hours
    days = hours / 24
    return "%d d" % days


@register.filter
def human_timesince(then):
    delta = datetime.now() - then
    return human_seconds(delta.days * 24 * 3600 + delta.seconds)
