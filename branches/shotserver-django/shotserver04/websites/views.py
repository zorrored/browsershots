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
from shotserver04.websites.models import Website
from shotserver04.browsers.models import Browser
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
    if url.isdigit():
        website = get_object_or_404(Website, id=int(url))
    else:
        if http_request.META['QUERY_STRING']:
            url += '?' + http_request.META['QUERY_STRING']
        website = get_object_or_404(Website, url=url)
    # Use caching to reduce number of SQL queries
    browsers = Browser.objects.all()
    preload_foreign_keys(browsers, browser_group=True)
    factories = Factory.objects.all()
    preload_foreign_keys(factories, operating_system=True)
    request_group_list = website.requestgroup_set.all()
    for request_group in request_group_list:
        request_group._browsers_cache = browsers
        request_group._factories_cache = factories
    # Get other websites on the same domain
    domain_website_list = website.domain.website_set.exclude(id=website.id)
    return render_to_response('websites/details.html', locals())
