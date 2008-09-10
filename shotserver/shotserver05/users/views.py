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
Views for the users app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.utils import simplejson
from django import forms
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

USERNAME_CHARS_FIRST = 'abcdefghijklmnopqrstuvwxyz'
USERNAME_CHARS = USERNAME_CHARS_FIRST + '0123456789_.-'
RESERVED_USERNAMES = 'admin administrator root webmaster postmaster'.split()
PASSWORD_MIN_LENGTH = 6


class UserCreateForm(forms.Form):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    repeat = forms.CharField(max_length=40, widget=forms.PasswordInput)
    email = forms.EmailField()

    class Media:
        js = ("/static/js/jquery.js",
              "/static/js/jquery.form.js")

    def clean_first_name(self):
        """
        Check that the first name starts with an uppercase letter.
        """
        first_name = self.cleaned_data['first_name']
        if not first_name:
            return ''
        if not first_name[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            raise forms.ValidationError(
                "Name should start with a capital letter.")
        if len(first_name) > 4 and first_name.upper() == first_name:
            raise forms.ValidationError(
                "Name should not be all uppercase.")
        return first_name

    def clean_last_name(self):
        """
        Check that the last name starts with an uppercase letter.
        """
        last_name = self.cleaned_data['last_name']
        if not last_name:
            return ''
        if not last_name[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            raise forms.ValidationError(
                "Name should start with a capital letter.")
        if len(last_name) > 4 and last_name.upper() == last_name:
            raise forms.ValidationError(
                "Name should not be all uppercase.")
        return last_name

    def clean_username(self):
        """
        Check that the username is sensible and available.
        """
        username = self.cleaned_data['username']
        if username[0] not in USERNAME_CHARS_FIRST:
            raise forms.ValidationError(
                "Username must start with a lowercase letter.")
        for index in range(len(username)):
            if username[index] not in USERNAME_CHARS:
                raise forms.ValidationError(
                    "Username may contain only simple letters (a-z0-9_.-).")
        if username in RESERVED_USERNAMES:
            raise forms.ValidationError("This username is reserved.")
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


def register(request):
    form = UserCreateForm(request.POST or None)
    if not form.is_valid():
        form_focus = 'first_name'
        for field in form.fields:
            if field in form.errors:
                form_focus = field
                break
        return render_to_response('users/register.html', locals(),
            context_instance=RequestContext(request))
    return HttpResponse('OK', 'text/plain')


def validate(request, field_name):
    form = UserCreateForm(request.POST or None)
    response = {field_name: ''}
    if field_name in form.errors:
        response[field_name] = unicode(form.errors[field_name][0])
    if field_name == 'password':
        response['repeat'] = ''
        if 'repeat' in form.errors:
            response['repeat'] = unicode(form.errors['repeat'][0])
    return HttpResponse(simplejson.dumps(response), 'application/json')
