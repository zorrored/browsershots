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
postmaster test testuser testclient staff create
""".split()


class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    username = forms.RegexField(min_length=2, max_length=40,
        regex=r'[a-z][a-z0-9-_]+')
    password = forms.CharField(min_length=6, max_length=40,
        widget=forms.PasswordInput)
    repeat = forms.CharField(max_length=40,
        widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_first_name(self):
        """
        Check that the first name starts with an uppercase letter.
        """
        first_name = self.cleaned_data['first_name']
        if first_name[0].upper() != first_name[0]:
            raise forms.ValidationError("Name must start with uppercase.")
        return first_name

    def clean_last_name(self):
        """
        Check that the last name starts with an uppercase letter.
        """
        last_name = self.cleaned_data['last_name']
        if last_name[0].upper() != last_name[0]:
            raise forms.ValidationError("Name must start with uppercase.")
        return last_name

    def clean_username(self):
        """
        Check that the username is sensible and available.
        """
        username = self.cleaned_data['username']
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("This username is reserved.")
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        """
        Check that the password is not too silly.
        """
        password = self.cleaned_data['password']
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

    def save(self):
        """
        Create a new user with the form data.
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
