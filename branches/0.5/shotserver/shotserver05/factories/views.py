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

from django.shortcuts import render_to_response
from django.http import HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import get_object_or_404
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


def auth_html(request, name):
    """
    Get HTML file with secret key for XML-RPC authentication.
    """
    factory = get_object_or_404(Factory, name=name)
    if request.user != factory.user and factory.user.username != 'testclient':
        return HttpResponseForbidden('Forbidden', 'text/plain')
    return render_to_response('factories/auth.html', locals(),
        context_instance=RequestContext(request))
