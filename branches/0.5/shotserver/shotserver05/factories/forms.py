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
from shotserver05.factories.models import Factory

LOWERCASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
FACTORY_NAME_CHARS = LOWERCASE_LETTERS + DIGITS + '_-'
RESERVED_FACTORY_NAMES = """
add auth validate
""".split()


class CreateFactoryForm(forms.ModelForm):
    """
    Create a new screenshot factory.
    """
    hardware = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    class Meta:
        model = Factory
        exclude = ('user', 'secret_key')

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) == 0:
            raise forms.ValidationError("This field is required.")
        if len(name) < 2:
            raise forms.ValidationError(
                "Factory name must be at least 2 characters long.")
        if name[0] not in LOWERCASE_LETTERS:
            raise forms.ValidationError(
                "Factory name must start with a lowercase letter.")
        for letter in name[0]:
            if letter not in FACTORY_NAME_CHARS:
                raise forms.ValidationError(
"Factory name may contain only lowercase letters, digits, hyphen, underscore.")
        return name

    def clean_hardware(self):
        hardware = self.cleaned_data['hardware'].strip()
        if len(hardware) == 0:
            raise forms.ValidationError("This field is required.")
        return hardware


class FactoryForm(forms.ModelForm):
    """
    Edit factory details.
    """
    hardware = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

    clean_hardware = CreateFactoryForm.clean_hardware

    class Meta:
        model = Factory
        exclude = ('name', 'user', 'secret_key')
