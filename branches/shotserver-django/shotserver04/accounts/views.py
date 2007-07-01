# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.

"""
Account views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from shotserver04.factories.models import Factory
from shotserver04.messages.models import FactoryError


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
    return render_to_response('accounts/profile.html', locals())
