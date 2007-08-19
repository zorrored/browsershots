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
Website views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.core.paginator import ObjectPaginator
from shotserver04.websites.models import Website
from shotserver04.browsers.models import Browser, BrowserGroup
from shotserver04.factories.models import Factory
from shotserver04.common.preload import preload_foreign_keys


def overview(http_request):
    """
    List websites, with keyword search filter.
    """
    website_list = Website.objects
    search_query = http_request.GET.get('q', '')
    for search in search_query.split():
        if search.islower(): # Case insensitive search
            website_list = website_list.filter(url__icontains=search)
        else: # Case sensitive search if mixed case in query
            website_list = website_list.filter(url__contains=search)
    website_list = website_list.order_by('-submitted')
    website_list = website_list[:100]
    return render_to_response('websites/overview.html', locals())


def details(http_request, url):
    """
    Show details for a selected website.
    """
    page = 1
    if url.isdigit():
        website = get_object_or_404(Website, id=int(url))
        if 'page' in http_request.GET:
            page = int(http_request.GET['page'])
    else:
        if http_request.META['QUERY_STRING']:
            url += '?' + http_request.META['QUERY_STRING']
        website = get_object_or_404(Website, url=url)
    # Use caching to reduce number of SQL queries
    domain = website.domain
    browser_groups = BrowserGroup.objects.all()
    browsers = Browser.objects.all()
    preload_foreign_keys(browsers, browser_group=browser_groups)
    factories = Factory.objects.all()
    preload_foreign_keys(factories, operating_system=True)
    request_groups = list(website.requestgroup_set.all())
    paginator = ObjectPaginator(request_groups, num_per_page=5, orphans=2)
    if page < 1 or page > paginator.pages:
        raise Http404('Requested page out of range.')
    request_group_list = paginator.get_page(page - 1)
    pages_list = []
    if paginator.pages > 1:
        for number in range(1, paginator.pages + 1):
            extra_classes = ''
            if page == number:
                extra_classes = ' current'
            pages_list.append(
                u'<a class="page%s" href="%s?page=%d">%d</a>' % (
                extra_classes, website.get_numeric_url(), number, number))
    for index, request_group in enumerate(request_groups):
        request_group._index = len(request_groups) - index
        request_group._browser_groups_cache = browser_groups
        request_group._browsers_cache = browsers
        request_group._factories_cache = factories
        request_group._website_cache = website
        request_group._website_cache._domain_cache = domain
    # Get other websites on the same domain
    domain_website_list = domain.website_set.exclude(id=website.id)
    return render_to_response('websites/details.html', locals())
