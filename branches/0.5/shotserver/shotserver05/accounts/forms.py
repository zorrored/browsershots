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
Forms for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import forms
from django.contrib.auth.models import User

RESERVED_USERNAMES = """
admin administrator root webmaster www-data
postmaster test testuser testclient staff auth add register
""".split()
LOWERCASE_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
USERNAME_CHARS = LOWERCASE_LETTERS + DIGITS + '_-'
USERNAME_MIN_LENGTH = 2
PASSWORD_MIN_LENGTH = 6


class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    repeat = forms.CharField(max_length=40, widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_first_name(self):
        """
        Check that the first name starts with an uppercase letter.
        """
        first_name = self.cleaned_data['first_name'].strip()
        if not first_name:
            return ''
        if first_name[0].upper() != first_name[0]:
            raise forms.ValidationError("Name should start with uppercase.")
        return first_name

    def clean_last_name(self):
        """
        Check that the last name starts with an uppercase letter.
        """
        last_name = self.cleaned_data['last_name'].strip()
        if not last_name:
            return ''
        if last_name[0].upper() != last_name[0]:
            raise forms.ValidationError("Name should start with uppercase.")
        return last_name

    def clean_username(self):
        """
        Check that the username is sensible and available.
        """
        username = self.cleaned_data['username'].strip()
        if len(username) < USERNAME_MIN_LENGTH:
            raise forms.ValidationError(
                "The username must have at least %d characters." %
                USERNAME_MIN_LENGTH)
        if username[0] not in LOWERCASE_LETTERS:
            raise forms.ValidationError(
                "Username must start with a lowercase letter.")
        for index in range(len(username)):
            if username[index] not in USERNAME_CHARS:
                raise forms.ValidationError(
                    "Username may contain only simple letters (a-z0-9_.-).")
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("This username is reserved.")
        print 'validating username'
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        """
        Check that the password is long enough and not too silly.
        """
        password = self.cleaned_data['password']
        if len(password) < PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(
                "The password must have at least %d characters." %
                PASSWORD_MIN_LENGTH)
        if password.isdigit() or password == len(password) * password[0]:
            raise forms.ValidationError("The password is too simple.")
        return password

    def clean_repeat(self):
        """
        Check that the password and repeat is the same.
        """
        if 'password' not in self.cleaned_data:
            return
        password = self.cleaned_data['password']
        repeat = self.cleaned_data['repeat']
        if repeat != password:
            raise forms.ValidationError("Enter the same password again.")
        return repeat
