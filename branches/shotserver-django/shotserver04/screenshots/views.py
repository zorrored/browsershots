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
Screenshot views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.shortcuts import render_to_response, get_object_or_404
from shotserver04.screenshots.models import Screenshot
from shotserver04.requests.models import Request

COLUMNS = 11


def screenshot_list(request):
    columns = [[0, index * 88] for index in range(COLUMNS)]
    previews = []
    for screenshot in Screenshot.objects.recent():
        width = 80
        height = screenshot.height * width / screenshot.width
        columns.sort()
        top, left = columns[0]
        previews.append(
            screenshot.preview_div(
            style="left:%dpx;top:%dpx;position:absolute" % (left, top),
            title=screenshot.website.url,
            href=screenshot.website.get_absolute_url()))
        columns[0][0] += height + 8
    columns.sort()
    previews.insert(0,
        '<div class="previews" style="height:%dpx">' % columns[-1][0])
    previews.append('</div>')
    previews = '\n'.join(previews)
    return render_to_response('screenshots/screenshot_list.html', locals())


def screenshot_detail(request, hashkey):
    screenshot = get_object_or_404(Screenshot, hashkey=hashkey)
    request = Request.objects.get(screenshot=screenshot)
    return render_to_response('screenshots/screenshot_detail.html', locals())
