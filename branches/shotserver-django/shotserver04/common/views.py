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
Browsershots front page.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from shotserver04.common import int_or_none, last_poll_timeout
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.common.forms.url import UrlForm
from shotserver04.common.forms.browsers import BrowsersForm
from shotserver04.common.forms.features import FeaturesForm
from shotserver04.common.forms.options import OptionsForm
from shotserver04.factories.models import Factory
from shotserver04.platforms.models import Platform, OperatingSystem
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.requests.models import RequestGroup, Request

BROWSER_COLUMNS = 5


def start(http_request):
    """
    Front page with URL input, browser chooser, and options.
    """
    # Initialize forms.
    post = http_request.POST or None
    url_form = UrlForm(post)
    features_form = FeaturesForm(post)
    options_form = OptionsForm(post)
    # Get available choices from database, with correct translations.
    active_factories = Factory.objects.filter(
        last_poll__gte=last_poll_timeout())
    active_browsers = Browser.objects.filter(
        factory__in=active_factories,
        active=True)
    if not active_browsers:
        error_title = _("out of service")
        error_message = ' '.join((
            _("No active screenshot factories."),
            _("Please try again later."),
            ))
        return render_to_response('error.html', locals())
    features_form.load_choices(active_browsers)
    options_form.load_choices(active_factories)
    # Validate posted data.
    valid_post = (url_form.is_valid() and
                  options_form.is_valid() and
                  features_form.is_valid())
    # Preload some database entries for browser forms
    preload_foreign_keys(active_browsers,
                         factory=active_factories,
                         factory__operating_system=True,
                         browser_group=True)
    # Browser forms for each platform.
    browser_forms = []
    for platform in Platform.objects.all():
        browser_form = BrowsersForm(active_browsers, platform, post)
        if browser_form.is_bound:
            browser_form.full_clean()
        if browser_form.fields:
            browser_forms.append(browser_form)
        valid_post = valid_post and browser_form.is_valid()
    browser_forms[0].is_first = True
    browser_forms[-1].is_last = True
    if not valid_post:
        # Show HTML form.
        if 'url' in http_request.GET:
            url_form.fields['url'].initial = http_request.GET['url']
        multi_column(browser_forms)
        return render_to_response('start.html', locals())
    # Create screenshot requests and redirect to website overview.
    values = {
        'ip': http_request.META['REMOTE_ADDR'],
        'website': url_form.cleaned_data['website'],
        'expire': datetime.now() + timedelta(minutes=30),
        }
    values.update(options_form.cleaned_dict())
    values.update(features_form.cleaned_dict())
    request_group = RequestGroup.objects.create(**values)
    for browser_form in browser_forms:
        create_platform_requests(
            request_group, browser_form.platform, browser_form)
    # Make sure that the redirect will show the new request group
    transaction.commit()
    # return render_to_response('debug.html', locals())
    return HttpResponseRedirect(values['website'].get_absolute_url())


def multi_column(browser_forms):
    groups = [[form.column_length(), form] for form in browser_forms]
    for total_columns in range(len(browser_forms), BROWSER_COLUMNS):
        groups.sort()
        length, form = groups[-1]
        if length <= 4:
            break
        form.columns += 1
        groups[-1][0] = form.column_length()


def create_platform_requests(request_group, platform, browser_form):
    """
    Create screenshots requests for selected browsers on one platform.
    """
    platform_lower = platform.name.lower().replace(' ', '-')
    result = []
    for name in browser_form.fields:
        if not browser_form.cleaned_data[name]:
            continue # Browser not selected
        first_part, browser_name, major, minor = name.split('_')
        if first_part != platform_lower:
            continue # Different platform
        browser_group = BrowserGroup.objects.get(
            name__iexact=browser_name.replace('-', ' '))
        result.append(Request.objects.create(
            request_group=request_group,
            platform=platform,
            browser_group=browser_group,
            major=int_or_none(major),
            minor=int_or_none(minor),
            ))
    return result
