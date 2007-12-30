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
Browsershots front page.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import urllib
from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from shotserver04.common import int_or_none, last_poll_timeout, error_page
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.start.models import NewsItem
from shotserver04.start.forms.url import UrlForm
from shotserver04.start.forms.browsers import BrowsersForm
from shotserver04.start.forms.features import FeaturesForm
from shotserver04.start.forms.options import OptionsForm
from shotserver04.start.forms.special import SpecialForm
from shotserver04.factories.models import Factory
from shotserver04.platforms.models import Platform
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.requests.models import RequestGroup, Request
from shotserver04.sponsors.models import Sponsor

BROWSER_COLUMNS = 5
SELECTOR_TEMPLATE = u"""
<a href="javascript:select_browsers('%s')" onfocus="this.blur()">%s</a>
""".strip()


def start(http_request):
    """
    Front page with URL input, browser chooser, and options.
    """
    if (http_request.user.is_anonymous() and
        hasattr(settings, 'ALLOW_ANONYMOUS_REQUESTS') and
        not settings.ALLOW_ANONYMOUS_REQUESTS):
        url = '/'
        if http_request.META['QUERY_STRING']:
            url += '?' + http_request.META['QUERY_STRING']
        return error_page(http_request, _("login required"),
            _("Anonymous screenshot requests are not allowed."),
            u'<a href="/accounts/login/?next=%s">%s</a>' % (
                urllib.quote(url),
                _("Please log in with your username and password.")))
    # Initialize forms.
    post = http_request.POST or None
    url_form = UrlForm(post)
    features_form = FeaturesForm(post)
    options_form = OptionsForm(post)
    special_form = SpecialForm(post)
    # Get available choices from database, with correct translations.
    active_factories = Factory.objects.filter(
        last_poll__gte=last_poll_timeout())
    active_browsers = Browser.objects.filter(
        factory__in=active_factories,
        active=True)
    if not active_browsers:
        return error_page(http_request, _("out of service"),
            _("No active screenshot factories."),
            _("Please try again later."))
    features_form.load_choices(active_browsers)
    options_form.load_choices(active_factories)
    # Validate posted data.
    valid_post = (url_form.is_valid() and
                  options_form.is_valid() and
                  features_form.is_valid() and
                  special_form.is_valid())
    # Preload some database entries for browser forms
    preload_foreign_keys(active_browsers,
                         factory=active_factories,
                         factory__operating_system=True,
                         browser_group=True,
                         engine=True)
    # Select browsers according to GET request
    selected_browsers = None
    if 'browsers' in http_request.GET:
        selected_browsers = http_request.GET['browsers'].split()
    # Browser forms for each platform.
    browser_forms = []
    for platform in Platform.objects.all():
        browser_form = BrowsersForm(active_browsers, platform,
                                    post, selected_browsers)
        browser_form.platform_name = \
            unicode(platform).lower().replace(' ', '-')
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
        selectors = mark_safe(',\n'.join([
            SELECTOR_TEMPLATE % (plus_minus, capfirst(text))
            for text, plus_minus in selector_pairs(browser_forms)]))
        news_list = NewsItem.objects.all()[:10]
        sponsors_list = Sponsor.objects.filter(front_page=True)
        show_special_form = http_request.user.is_authenticated()
        return render_to_response('start/start.html', locals(),
            context_instance=RequestContext(http_request))
    # Create screenshot requests and redirect to website overview.
    expire = datetime.now() + timedelta(minutes=30)
    values = {
        'website': url_form.cleaned_data['website'],
        'ip': http_request.META['REMOTE_ADDR'],
        'user': None,
        }
    if http_request.user.is_authenticated():
        values['user'] = http_request.user
    values.update(options_form.cleaned_data)
    values.update(features_form.cleaned_data)
    values.update(special_form.cleaned_data)
    match_values = {}
    for key in values:
        if values[key] is None:
            match_values[key + '__isnull'] = True
        else:
            match_values[key] = values[key]
    existing = RequestGroup.objects.filter(
        expire__gte=datetime.now(), **match_values).order_by('-submitted')
    if (len(existing) and
        existing[0].request_set.filter(screenshot__isnull=True).count()):
        # Previous request group is still pending, reuse it.
        request_group = existing[0]
        request_group.update_fields(expire=expire)
    else:
        request_group = RequestGroup.objects.create(expire=expire, **values)
    # Get priority processing for domain or user.
    priority = 0
    if 'shotserver04.priority' in settings.INSTALLED_APPS:
        from shotserver04.priority import domain_priority, user_priority
        priority = max(domain_priority(url_form.cleaned_data['domain']),
                       user_priority(http_request.user))
    for browser_form in browser_forms:
        create_platform_requests(
            request_group, browser_form.platform, browser_form, priority)
    # Make sure that the redirect will show the new request group
    transaction.commit()
    # return render_to_response('debug.html', locals(),
    #     context_instance=RequestContext(http_request))
    return HttpResponseRedirect(values['website'].get_absolute_url())


def multi_column(browser_forms):
    """
    Arrange browsers in multiple columns per platform.
    """
    groups = [[form.column_length(), form] for form in browser_forms]
    for total_columns in range(len(browser_forms), BROWSER_COLUMNS):
        groups.sort()
        length, form = groups[-1]
        if length <= 4:
            break
        form.columns += 1
        groups[-1][0] = form.column_length()


def selector_pairs(browser_forms):
    """
    Links to select or unselect all browsers.
    """
    total = sum([len(form.fields) for form in browser_forms])
    yield (_('all'), '+' * total)
    yield (_('none'), '-' * total)
    start = 0
    for form in browser_forms:
        length = len(form.fields)
        end = start + length
        yield (form.platform.name,
               '-' * start + '+' * length + '-' * (total - end))
        start = end
    yield ('Gecko', selector_func(browser_forms, lambda field:
        field.browser.engine.name == 'Gecko'))
    yield ('KHTML/WebKit', selector_func(browser_forms, lambda field:
        field.browser.engine.name in ('KHTML', 'AppleWebKit')))


def selector_func(browser_forms, func):
    result = []
    for form in browser_forms:
        for name, field in form.fields.items():
            if func(field):
                result.append('+')
            else:
                result.append('-')
    return ''.join(result)


def create_platform_requests(request_group, platform, browser_form,
                             priority=0):
    """
    Create screenshots requests for selected browsers on one platform.
    """
    platform_lower = platform.name.lower().replace(' ', '-')
    for name in browser_form.fields:
        if not browser_form.cleaned_data[name]:
            continue # Browser not selected
        first_part, browser_name, major, minor = name.split('_')
        if first_part != platform_lower:
            continue # Different platform
        browser_group = BrowserGroup.objects.get(
            name__iexact=browser_name.replace('-', ' '))
        Request.objects.get_or_create(
            request_group=request_group,
            platform=platform,
            browser_group=browser_group,
            major=int_or_none(major),
            minor=int_or_none(minor),
            priority=priority,
            )
