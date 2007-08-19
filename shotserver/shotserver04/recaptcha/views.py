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
Recaptcha views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.shortcuts import render_to_response
from shotserver04 import settings
from shotserver04.recaptcha import captcha


def recaptcha(http_request):
    """
    Show reCAPTCHA callenge.
    """
    error = None
    if http_request.POST:
        challenge = http_request.POST['recaptcha_challenge_field']
        response = http_request.POST['recaptcha_response_field']
        remote_ip = http_request.META['REMOTE_ADDR']
        result = captcha.submit(challenge, response,
            settings.RECAPTCHA_PRIVATE_KEY, remote_ip)
        if not result.is_valid:
            error = result.error_code
    recaptcha_html = captcha.displayhtml(settings.RECAPTCHA_PUBLIC_KEY,
                                         options={'theme': 'blackglass'},
                                         error=error)
    return render_to_response('recaptcha/recaptcha.html', locals())
