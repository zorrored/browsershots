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
Forms for the factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import forms
from django.utils.translation import ugettext as _
from shotserver05.factories.models import Factory

FACTORY_NAME_REGEX = r'[a-z][a-z0-9-_]*'
RESERVED_FACTORY_NAMES = """
localhost server factory shotfactory create
""".split()


class CreateFactoryForm(forms.ModelForm):
    """
    Create a new screenshot factory.
    """
    name = forms.RegexField(regex=FACTORY_NAME_REGEX,
        error_messages={'invalid': "Factory name must match %s." %
                        FACTORY_NAME_REGEX},
        min_length=2,
        max_length=Factory._meta.get_field('name').max_length)
    hardware = forms.CharField(
        max_length=Factory._meta.get_field('hardware').max_length,
        widget=forms.TextInput(attrs={'size': '40'}))

    class Meta:
        model = Factory
        exclude = ('user', 'secret_key')

    def clean_name(self):
        """
        Check the submitted factory name value.
        """
        name = self.cleaned_data['name'].strip()
        if len(name) == 0:
            raise forms.ValidationError(_("This field is required."))
        if name in RESERVED_FACTORY_NAMES:
            raise forms.ValidationError(_("This name is reserved."))
        return name

    def clean_hardware(self):
        """
        Check the submitted hardware value.
        """
        hardware = self.cleaned_data['hardware'].strip()
        if len(hardware) == 0:
            raise forms.ValidationError(_("This field is required."))
        return hardware


class FactoryForm(forms.ModelForm):
    """
    Edit factory details.
    """
    hardware = forms.CharField(
        max_length=Factory._meta.get_field('hardware').max_length,
        widget=forms.TextInput(attrs={'size': '40'}))

    clean_hardware = CreateFactoryForm.clean_hardware

    class Meta:
        model = Factory
        exclude = ('name', 'user', 'secret_key')
