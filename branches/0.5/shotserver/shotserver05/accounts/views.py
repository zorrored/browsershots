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
Views for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from shotserver05.utils.views import success_page
from shotserver05.accounts.forms import CreateUserForm


def create(request):
    """
    Register a new user account.
    """
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return success_page(request, "Account created",
            "Your user account was created.",
            "You can log in with the link in the top right corner.")
    form_focus = 'first_name'
    for field in form.fields:
        if field in form.errors:
            form_focus = field
            break
    form_title = "Create a new user account"
    form_validate = '/accounts/create/validate/'
    form_submit = 'Create'
    # form_action = '/accounts/validate/username/'
    return render_to_response('form.html', locals(),
        context_instance=RequestContext(request))


def validate(request, field):
    """
    AJAX validator for user account registration form.
    """
    data = None
    if request.POST:
        data = dict(request.POST.items())
        if field != 'username':
            # Don't validate username when editing the other fields,
            # because database lookup for taken usernames is expensive.
            data['username'] = ''
    form = CreateUserForm(data)
    response = {field: ''}
    if field in form.errors:
        response[field] = unicode(form.errors[field][0])
    if field == 'password':
        response['repeat'] = ''
        if 'repeat' in form.errors:
            response['repeat'] = unicode(form.errors['repeat'][0])
    return HttpResponse(simplejson.dumps(response), 'application/json')


@login_required
def profile(request):
    """
    Private user profile.
    """
    return render_to_response('accounts/profile.html', locals(),
        context_instance=RequestContext(request))
