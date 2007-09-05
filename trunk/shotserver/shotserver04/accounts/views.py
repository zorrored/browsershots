# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Account views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.contrib.auth.decorators import login_required
from django import newforms as forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from shotserver04 import settings
from shotserver04.factories.models import Factory
from shotserver04.messages.models import FactoryError
from shotserver04.common.preload import preload_foreign_keys


@login_required
def profile(http_request):
    """
    Show a user's private profile page.
    """
    factory_table_header = Factory.table_header()
    factory_list = Factory.objects.select_related().filter(
        admin=http_request.user)
    error_list = FactoryError.objects.filter(
        factory__in=factory_list).order_by('-id')[:10]
    preload_foreign_keys(error_list, factory=factory_list)
    if 'shotserver04.points' in settings.INSTALLED_APPS:
        from shotserver04.points import views as points
        latest = points.latest_balance(http_request.user)
        current_balance = latest.current_balance()
    return render_to_response('accounts/profile.html', locals(),
        context_instance=RequestContext(http_request))


class RegistrationForm(forms.Form):
    email = forms.EmailField()


def register(http_request):
    form = RegistrationForm(http_request.POST or None)
    return render_to_response('accounts/register.html', locals(),
        context_instance=RequestContext(http_request))
