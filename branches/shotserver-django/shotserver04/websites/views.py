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


def website_list(http_request):
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
    return render_to_response('websites/website_list.html', locals())


def website_detail(http_request, website_url):
    """
    Show details for a selected website.
    """
    if isinstance(website_url, Website):
        website = website_url
    else:
        if http_request.META['QUERY_STRING']:
            website_url += '?' + http_request.META['QUERY_STRING']
        website = get_object_or_404(Website, url=website_url)
    domain_website_list = website.domain.website_set.exclude(id=website.id)
    return render_to_response('websites/website_detail.html', locals())


def website_numeric(http_request, website_id):
    """
    Show details for a website, selected by numeric ID not URL.
    """
    website = get_object_or_404(Website, id=website_id)
    return website_detail(http_request, website)
