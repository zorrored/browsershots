#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'

import cgi
from shotserver04.paypal.models import PayPalLog

for log in PayPalLog.objects.all():
    post = cgi.parse_qs(log.raw_post_data)
    business = post.get('payer_business_name', [''])[0]
    if business:
        print business
        log.update_fields(payer_business_name=business)
