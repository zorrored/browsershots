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
Factory views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.http import Http404
from django.utils.text import capfirst
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from shotserver04 import settings
from shotserver04.common import last_poll_timeout
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.screenshots.models import Screenshot, ProblemReport
from shotserver04.common.preload import preload_foreign_keys


def overview(http_request):
    """
    List all screenshot factories.
    """
    factory_table_header = Factory.table_header()
    factory_list = Factory.objects.select_related().filter(
        last_poll__gt=last_poll_timeout()).order_by('-uploads_per_day')
    if not len(factory_list):
        error_title = capfirst(_("out of service"))
        error_message = _("No active screenshot factories.")
        return render_to_response('error.html', locals())
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
    browser_list.sort(key=lambda browser: (unicode(browser), browser.id))
    screensize_list = factory.screensize_set.all()
    colordepth_list = factory.colordepth_set.all()
    screenshot_list = Screenshot.objects.filter(factory=factory,
        website__profanities__lte=settings.PROFANITIES_ALLOWED)
    screenshot_list = screenshot_list.order_by('-id')[:10]
    preload_foreign_keys(screenshot_list, browser=browser_list)
    admin_logged_in = http_request.user.id == factory.admin_id
    show_commands = admin_logged_in and True in [
        bool(browser.command) for browser in browser_list]
    problems_list = ProblemReport.objects.filter(
        screenshot__factory=factory)[:10]
    return render_to_response('factories/details.html', locals())


@login_required
def add(http_request):
    """
    Create a new screenshot factory.
    """
    return render_to_response('factories/edit.html', locals())
