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
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser

FACTORY_LIST_COLUMNS = (
    'name',
    'operating_system',
    'architecture',
    'last_poll',
    'last_upload',
    'uploads_per_hour',
    'uploads_per_day',
)


def factory_list(request):
    order = request.GET.get('order', '')
    if order.lstrip('-') not in FACTORY_LIST_COLUMNS:
        order = '-uploads_per_day'
    order_column = order.lstrip('-')
    descending = order.startswith('-')
    header_list = []
    for column in FACTORY_LIST_COLUMNS:
        text = Factory._meta.get_field(column).verbose_name
        if text.count('-'):
            text = text.replace('-', '-<br />', 1)
        else:
            text = text.replace(' ', '<br />', 1)
        class_attrib = ''
        if column == order_column:
            if descending:
                class_attrib = ' class="sorted descending"'
                url = '?order=' + column
            else:
                class_attrib = ' class="sorted ascending"'
                url = '?order=-' + column
        else:
            url = '?order=' + column
        header_list.append({'text': text,
                            'url': url,
                            'class_attrib': class_attrib})
    factory_list = list(Factory.objects.select_related().order_by(
        order, 'name'))
    return render_to_response('factories/factory_list.html', locals())


def factory_detail(request, factory_name):
    try:
        factory = Factory.objects.get(name=factory_name)
    except Factory.DoesNotExist:
        raise Http404
    browser_list = Browser.objects.select_related().filter(factory=factory.id)
    screensize_list = factory.screensize_set.all()
    colordepth_list = factory.colordepth_set.all()
    return render_to_response('factories/factory_detail.html', locals())
