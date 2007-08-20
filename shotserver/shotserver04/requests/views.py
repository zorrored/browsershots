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

from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from shotserver04.requests.models import Request, RequestGroup
from shotserver04.platforms.models import Platform
from shotserver04.browsers.models import BrowserGroup, Browser


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
    browsers = Browser.objects.filter(browser_group__in=browser_group_ids)
    browser_list = []
    for key in browser_requests.keys():
        platform_id, browser_group_id, major, minor = key
        uploads_per_hour = sum([b.uploads_per_hour for b in browsers
            if b.browser_group_id == browser_group_id
            and b.major == major and b.minor == minor
            and b.uploads_per_hour])
        uploads_per_day = sum([b.uploads_per_day for b in browsers
            if b.browser_group_id == browser_group_id
            and b.major == major and b.minor == minor
            and b.uploads_per_day])
        browser_list.append({
            'platform': platforms[platform_id],
            'browser_group': browser_groups[browser_group_id],
            'major': major,
            'minor': minor,
            'uploads_per_hour': uploads_per_hour or '',
            'uploads_per_day': uploads_per_day or '',
            'pending_requests': browser_requests[key],
            })
    return render_to_response('requests/overview.html', locals())


def details(http_request, request_group_id):
    """
    Show details about the selected request group.
    """
    request_group = get_object_or_404(RequestGroup, id=request_group_id)
    website = request_group.website
    return render_to_response('requests/details.html', locals())


def extend(http_request):
    """
    Extend the expiration timeout of a screenshot request group.
    """
    error_title = "Invalid request"
    if not http_request.POST:
        error_message = "You must send a POST request to this page."
        return render_to_response('error.html', locals())
    try:
        request_group_id = int(http_request.POST['request_group_id'])
    except (KeyError, ValueError):
        error_message = "You must specify a numeric request group ID."
        return render_to_response('error.html', locals())
    request_group = get_object_or_404(RequestGroup, pk=request_group_id)
    request_group.expire = datetime.now() + timedelta(minutes=30)
    request_group.save()
    return HttpResponseRedirect(http_request.META['HTTP_REFERER'])
