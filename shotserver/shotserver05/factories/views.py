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
Views for the factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.utils import simplejson
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from shotserver05.factories.models import Factory
from shotserver05.factories.forms import FactoryForm


def index(request):
    """
    List active screenshot factories.
    """
    return render_to_response('factories/index.html', locals(),
        context_instance=RequestContext(request))


def details(request, name):
    """
    Show details for a specified factory.
    """
    factory = get_object_or_404(Factory, name=name)
    form = FactoryForm(instance=factory)
    return render_to_response('factories/details.html', locals(),
        context_instance=RequestContext(request))


@login_required
def create(request):
    """
    Register a new screenshot factory.
    """
    form = FactoryForm(request.POST or None)
    if form.is_valid():
        factory = form.save(commit=False)
        factory.user = request.user
        factory.save()
        return HttpResponseRedirect('/factories/%s/' % factory.name)
    form_title = "Register a new screenshot factory"
    form_focus = 'name'
    for field in form.fields:
        if field in form.errors:
            form_focus = field
            break
    form_submit = "Register"
    form_validate = '/factories/create/validate/'
    return render_to_response('form.html', locals(),
        context_instance=RequestContext(request))


def create_validate(request, field):
    """
    AJAX validator for the factory registration form.
    """
    data = None
    if request.POST:
        data = dict(request.POST.items())
        if field != 'name':
            # Don't validate name when editing the other fields,
            # because database lookup for taken factory names is expensive.
            data['name'] = ''
    form = FactoryForm(data)
    response = {field: ''}
    if field in form.errors:
        response[field] = unicode(form.errors[field][0])
    return HttpResponse(simplejson.dumps(response), 'application/json')
