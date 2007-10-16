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
Request views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import urllib
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext as _
from shotserver04.common import last_poll_timeout, error_page
from shotserver04.requests.models import Request, RequestGroup
from shotserver04.platforms.models import Platform
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.common.templatetags import human


def overview(http_request):
    """
    Show statistics about pending requests.
    """
    requests = Request.objects.filter(
        screenshot__isnull=True,
        request_group__expire__gt=datetime.now())
    browser_requests = {}
    platform_ids = set()
    browser_group_ids = set()
    for request in requests:
        browser = (request.platform_id, request.browser_group_id,
                   request.major, request.minor)
        browser_requests[browser] = browser_requests.get(browser, 0) + 1
        platform_ids.add(request.platform_id)
        browser_group_ids.add(request.browser_group_id)
    platforms = dict([(p.id, p)
        for p in Platform.objects.filter(id__in=platform_ids)])
    browser_groups = dict([(b.id, b)
        for b in BrowserGroup.objects.filter(id__in=browser_group_ids)])
    browsers = Browser.objects.filter(
        browser_group__in=browser_group_ids,
        uploads_per_day__gt=0)
    preload_foreign_keys(browsers, factory__operating_system=True)
    browser_list = []
    for key in browser_requests.keys():
        platform_id, browser_group_id, major, minor = key
        uploads_per_hour, uploads_per_day = count_uploads(
            browsers, platform_id, browser_group_id, major, minor)
        browser_list.append({
            'platform': platforms[platform_id],
            'browser_group': browser_groups[browser_group_id],
            'major': major,
            'minor': minor,
            'uploads_per_hour': uploads_per_hour or '',
            'uploads_per_day': uploads_per_day or '',
            'pending_requests': browser_requests[key],
            })
    return render_to_response('requests/overview.html', locals(),
        context_instance=RequestContext(http_request))


def count_uploads(browsers, platform_id, browser_group_id, major, minor):
    """
    Count uploads per hour and per day from all matching browsers.
    """
    uploads_per_hour = uploads_per_day = 0
    for b in browsers:
        if (b.factory.operating_system.platform_id == platform_id
            and b.browser_group_id == browser_group_id
            and b.major == major and b.minor == minor):
            if b.uploads_per_hour:
                uploads_per_hour += b.uploads_per_hour
            if b.uploads_per_day:
                uploads_per_day += b.uploads_per_day
    return uploads_per_hour, uploads_per_day


def queue_estimate(request, active_browsers, queued_seconds):
    """
    Remaining queue estimate for the fastest matching browser for this request.
    """
    estimates = []
    for browser in active_browsers:
        if (browser.factory.operating_system.platform_id ==
                request.platform_id and
            browser.browser_group_id == request.browser_group_id and
            (browser.major == request.major or request.major is None) and
            (browser.minor == request.minor or request.minor is None)):
            estimate = browser.factory.queue_estimate
            if estimate:
                estimates.append(estimate)
    if not estimates:
        return _("unavailable")
    seconds = max(60, min(estimates) - queued_seconds)
    minutes = (seconds + 30) / 60
    return _("%(minutes)d min") % {'minutes': minutes}


def details(http_request, request_group_id):
    """
    Show details about the selected request group.
    """
    request_group = get_object_or_404(RequestGroup, id=request_group_id)
    now = datetime.now()
    expired = request_group.expire < now
    queued = now - request_group.submitted
    queued_seconds = queued.seconds + queued.days * 24 * 3600
    website = request_group.website
    active_factories = Factory.objects.filter(
        last_poll__gte=last_poll_timeout())
    active_browsers = Browser.objects.filter(
        factory__in=active_factories,
        active=True)
    browser_groups = BrowserGroup.objects.all()
    preload_foreign_keys(active_browsers, browser_group=browser_groups,
        factory=active_factories, factory__operating_system=True)
    requests = request_group.request_set.all()
    preload_foreign_keys(requests, browser_group=browser_groups)
    platform_queue_estimates = []
    for platform in Platform.objects.all():
        estimates = []
        for request in requests:
            if request.platform_id == platform.id:
                status = (request.status() or
                    (expired and _("expired")) or
                    queue_estimate(request, active_browsers, queued_seconds))
                estimates.append({
                    'browser': request.browser_string(),
                    'status': status,
                    })
        if estimates:
            estimates.sort()
            platform_queue_estimates.append((platform, estimates))
    return render_to_response('requests/details.html', locals(),
        context_instance=RequestContext(http_request))


def extend(http_request):
    """
    Extend the expiration timeout of a screenshot request group.
    """
    if not http_request.POST:
        return error_page(http_request, _("invalid request"),
            _("You must send a POST request to this page."))
    try:
        request_group_id = int(http_request.POST['request_group_id'])
    except (KeyError, ValueError):
        return error_page(http_request, _("invalid request"),
            _("You must specify a numeric request group ID."))
    request_group = get_object_or_404(RequestGroup, pk=request_group_id)
    if request_group.expire < datetime.now():
        delta = datetime.now() - request_group.expire
        minutes = min(1, delta.seconds / 60 + delta.days * 24 * 60)
        return error_page(http_request, _("request group expired"),
            _("This request group already expired %d minutes ago.") % minutes,
            '<a href="/?url=%s">%s</a>' % (
                urllib.quote(request_group.website.url),
                _("Request new screenshots?")))
    request_group.expire = datetime.now() + timedelta(minutes=30)
    request_group.save()
    return HttpResponseRedirect(request_group.website.get_absolute_url())
