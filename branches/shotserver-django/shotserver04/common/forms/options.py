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
Input form with select fields for screen size, color depth, timeout.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms
from shotserver04.factories.models import ScreenSize, ColorDepth
from shotserver04.common import last_poll_timeout, int_or_none
from shotserver04.common import lazy_gettext_capfirst as _
from datetime import datetime, timedelta


def screen_size_choices():
    """
    Get screen sizes that are supported by active factories.
    """
    yield ('dontcare', _("don't care"))
    previous = None
    for size in ScreenSize.objects.filter(
        factory__last_poll__gt=last_poll_timeout()):
        if size != previous:
            yield (size.width, str(size))
            previous = size


def color_depth_choices():
    """
    Get color depths that are supported by active factories.
    """
    yield ('dontcare', _("don't care"))
    previous = None
    for depth in ColorDepth.objects.filter(
        factory__last_poll__gt=last_poll_timeout()):
        if depth != previous:
            yield (depth.bits_per_pixel, str(depth))
            previous = depth


class OptionsForm(forms.Form):
    """
    Request options input form.
    """
    screen_size = forms.ChoiceField(
        label=_("screen size"),
        initial='dontcare',
        choices=screen_size_choices())
    color_depth = forms.ChoiceField(
        label=_("color depth"),
        initial='dontcare',
        choices=color_depth_choices())
    maximum_wait = forms.ChoiceField(
        label=_("maximum wait"),
        initial=30, choices=(
        (15, _("15 minutes")),
        (30, _("30 minutes")),
        (60, _("1 hour")),
        (120, _("2 hours")),
        (240, _("4 hours")),
        ))

    def cleaned_dict(self):
        """
        Convert options to integer and timestamp.
        """
        return {
            'expire': datetime.now() + timedelta(
                minutes=int(self.cleaned_data['maximum_wait'])),
            'width': int_or_none(self.cleaned_data['screen_size']),
            'bits_per_pixel': int_or_none(self.cleaned_data['color_depth']),
            }
