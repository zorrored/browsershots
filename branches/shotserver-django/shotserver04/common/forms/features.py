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
Input form with select fields for Javascript, Java, Flash.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms
from shotserver04.browsers.models import Browser
from shotserver04.features.models import Javascript, Java, Flash
from shotserver04.common import last_poll_timeout
from shotserver04.common import lazy_gettext_capfirst as _


def feature_choices(model):
    """
    Get choices for a feature from the database.
    """
    yield ('dontcare', _("don't care"))
    timeout = last_poll_timeout()
    for version in model.objects.all():
        filters = {'factory__last_poll__gt': timeout}
        if version.version == 'enabled':
            filters[model._meta.module_name + '__id__gte'] = 2
        else:
            filters[model._meta.module_name + '__id'] = version.id
        if not Browser.objects.filter(**filters).count():
            continue
        if version.version == 'disabled':
            yield (version.version, _("disabled"))
        elif version.version == 'enabled':
            yield (version.version, _("enabled"))
        else:
            yield (version.version, version.version)


def feature_or_none(model, value):
    """
    Find feature instance by post value.
    """
    if value == 'dontcare':
        return None
    return model.objects.get(version=value)


class FeaturesForm(forms.Form):
    """
    Request features input form.
    """
    javascript = forms.ChoiceField(
        label=_("Javascript"), initial='dontcare')
    java = forms.ChoiceField(
        label=_("Java"), initial='dontcare')
    flash = forms.ChoiceField(
        label=_("Flash"), initial='dontcare')

    def load_choices(self):
        """
        Load available choices from the database.
        """
        self['javascript'].field.choices = feature_choices(Javascript)
        self['java'].field.choices = feature_choices(Java)
        self['flash'].field.choices = feature_choices(Flash)

    def cleaned_dict(self):
        """
        Get features from their tables.
        """
        return {
            'javascript': feature_or_none(
                Javascript, self.cleaned_data['javascript']),
            'java': feature_or_none(
                Java, self.cleaned_data['java']),
            'flash': feature_or_none(
                Flash, self.cleaned_data['flash']),
            }
