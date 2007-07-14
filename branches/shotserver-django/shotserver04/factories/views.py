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
Factory views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.http import Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from shotserver04 import settings
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.screenshots.models import Screenshot
from shotserver04.common.preload import preload_foreign_keys


def overview(http_request):
    """
    List all screenshot factories.
    """
    factory_table_header = Factory.table_header()
    factory_list = Factory.objects.select_related().filter(
        uploads_per_day__gt=0).order_by('-uploads_per_day')
    return render_to_response('factories/overview.html', locals())


def details(http_request, name):
    """
    Get detailed information about a screenshot factory.
    """
    try:
        factory = Factory.objects.get(name=name)
    except Factory.DoesNotExist:
        raise Http404
    browser_list = list(Browser.objects.filter(factory=factory.id))
    preload_foreign_keys(browser_list,
                         browser_group=True,
                         engine=True,
                         javascript=True,
                         java=True,
                         flash=True)
    browser_list.sort(key=Browser.__unicode__)
    screensize_list = factory.screensize_set.all()
    colordepth_list = factory.colordepth_set.all()
    screenshot_list = Screenshot.objects.filter(factory=factory,
        website__profanities__lte=settings.PROFANITIES_ALLOWED)
    screenshot_list = screenshot_list.order_by('-id')[:10]
    preload_foreign_keys(screenshot_list, browser=browser_list)
    admin_logged_in = http_request.user.id == factory.admin_id
    show_commands = admin_logged_in and True in [
        bool(browser.command) for browser in browser_list]
    return render_to_response('factories/details.html', locals())


@login_required
def add(http_request):
    """
    Create a new screenshot factory.
    """
    return render_to_response('factories/edit.html', locals())
