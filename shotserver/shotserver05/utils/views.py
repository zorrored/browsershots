# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Useful helper views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.shortcuts import render_to_response
from django.template import RequestContext


def result_page(request, result_class, result_title, result_message,
                *extra_messages):
    """
    Render result page with title and message.
    """
    return render_to_response('result.html', locals(),
        context_instance=RequestContext(request))


def error_page(request, result_title, result_message, *extra_messages):
    """
    Render error page with title and message.
    """
    return result_page(request, 'error', result_title, result_message,
                       *extra_messages)


def success_page(request, result_title, result_message, *extra_messages):
    """
    Render success page with title and message.
    """
    return result_page(request, 'success', result_title, result_message,
                       *extra_messages)
