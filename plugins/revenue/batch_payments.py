#!/usr/bin/env python
# coding: utf-8
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
Monthly mass payment through PayPal.
"""

__revision__ = "$Rev: 2895 $"
__date__ = "$Date: 2008-06-14 14:29:10 -0700 (Sat, 14 Jun 2008) $"
__author__ = "$Author: johann $"

import sys
import os
sys.path.insert(0, '.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils.text import capfirst
from django.contrib.auth.models import User
from shotserver04.revenue.models import UserRevenue, UserPayment

payments = UserPayment.objects.filter(paypal_email__contains='@')
id_to_email = dict([(p.user_id, p.paypal_email) for p in payments])
users = User.objects.filter(id__in=id_to_email)
for user in users:
    transactions = (
        list(user.userrevenue_set.all()) +
        list(user.userpayment_set.all()) +
        list(user.userdonation_set.all()))
    if not transactions:
        continue
    transactions.sort(key=lambda t: t.date)
    balance = transactions[-1].balance
    if balance < 20:
        continue
    email = id_to_email[user.id]
    balance_comma = str(balance).replace('.', ',')
    print '\t'.join((email, balance_comma, 'EUR', user.username))
    payment = UserPayment.objects.create(
        user=user,
        paypal_email=email,
        currency='EUR',
        amount=-balance,
        euros=-balance,
        balance=0,
        date=datetime.now(),
        )
    print >> sys.stderr, payment
