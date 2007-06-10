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

from django.shortcuts import render_to_response
from shotserver04.screenshots.models import Screenshot


def screenshot_list(request):
    columns = [[0, index * 88] for index in range(10)]
    screenshot_list = Screenshot.objects.all()[:100]
    previews = []
    for screenshot in screenshot_list:
        width = 80
        height = screenshot.height * width / screenshot.width
        columns.sort()
        top, left = columns[0]
        previews.append(
            '<div class="preview absolute"' +
            ' style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (
                left, top, width, height) +
            screenshot.preview_img() +
            '</div>')
        columns[0][0] += height + 8
    columns.sort()
    previews.insert(0, '<div class="relative" style="height:%dpx">' %
                    columns[9][0])
    previews.append('</div>')
    previews = '\n'.join(previews)
    return render_to_response('screenshots/screenshot_list.html', locals())
