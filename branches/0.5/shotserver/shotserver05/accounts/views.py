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
from django.http import HttpResponse, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.models import User
from shotserver05.users.forms import UserCreateForm


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


def validate(request, field):
    data = None
    if request.POST:
        data = dict(request.POST.items())
        if field != 'username':
            # Don't validate username when editing the other fields,
            # because database lookup for taken usernames is expensive.
            data['username'] = ''
    form = UserCreateForm(data)
    response = {field: ''}
    if field in form.errors:
        response[field] = unicode(form.errors[field][0])
    if field == 'password':
        response['repeat'] = ''
        if 'repeat' in form.errors:
            response['repeat'] = unicode(form.errors['repeat'][0])
    return HttpResponse(simplejson.dumps(response), 'application/json')


def auth_html(request, username):
    """
    Get HTML file with encrypted user password for XML-RPC authentication.
    """
    user = get_object_or_404(User, username=username)
    if request.user != user and username != 'testclient':
        return HttpResponseForbidden('Forbidden', 'text/plain')
    return render_to_response('users/auth.html', locals(),
        context_instance=RequestContext(request))
