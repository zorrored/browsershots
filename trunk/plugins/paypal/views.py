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
Paypal views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import urllib2
from django.http import HttpResponse
from django.db import transaction
from django import newforms as forms
from django.shortcuts import render_to_response
from shotserver04 import settings
from shotserver04.paypal.models import PayPalLog


def ipn(http_request):
    """
    Process IPN (instant payment notification) from PayPal.
    """
    if not http_request.POST:
        if settings.DEBUG:
            form_title = "PayPal IPN test form"
            form_action = '/paypal/ipn/'
            form = PayPalForm()
            form_submit = 'Submit'
            return render_to_response('form.html', locals())
        else:
            error_title = "Invalid request"
            error_message = "You must send a POST request to this page."
            return render_to_response('error.html', locals())
    # Log post request in the database
    attributes = {'raw_post_data': http_request.raw_post_data}
    for field in PayPalLog._meta.fields:
        if field.name in http_request.POST:
            attributes[field.name] = http_request.POST[field.name]
    paypallog = PayPalLog.objects.create(**attributes)
    # Post data back to PayPal
    if int(http_request.POST.get('test_ipn', '0')):
        paypal_url = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
    else:
        paypal_url = 'https://www.paypal.com/cgi-bin/webscr'
    data = http_request.raw_post_data + '&cmd=_notify-validate'
    req = urllib2.Request(paypal_url, data=data)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    response = urllib2.urlopen(req).read()
    paypallog.response = response
    paypallog.save()
    transaction.commit()
    # Check the response
    if (response == 'VERIFIED' and
        http_request.POST['payment_status'] == 'Completed'):
        assert PayPalLog.objects.filter(
            txn_id=http_request.POST['txn_id']).count() == 1
        # assert http_request.POST['receiver_email'] == 'johann@browsershots.org'
        # assert http_request.POST['payment_currency'] == 'USD'
        # Transaction.create(
        #     receiver=User.objects.get(email=http_request.POST['payer_email']),
        #     points=int(float(http_request['payment_currency']) * 50))
    return HttpResponse(response, mimetype="text/plain")


class PayPalForm(forms.Form):
    """
    Simple form to generate POST requests for testing PayPal IPN.
    """
    txn_id = forms.CharField(initial='3Y366594SP996132H')
    payment_date = forms.CharField(initial='22:20:41 Jul 23, 2007 PDT')
    payer_id = forms.CharField(initial='UXJ9E3MSX72E4')
    payer_email = forms.EmailField(initial='payer@example.com')
    receiver_id = forms.CharField(initial='U24R4KFWJQF5J')
    receiver_email = forms.EmailField(initial='receiver@example.com')
    mc_currency = forms.CharField(initial='EUR')
    mc_gross = forms.CharField(initial='10.00')
    mc_fee = forms.CharField(initial='0.70')
    payment_status = forms.CharField(initial='Completed')
    test_ipn = forms.IntegerField(initial=1)
