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
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.contrib.auth.models import User
from shotserver04.factories.models import Factory
from shotserver04.common import granular_update


class UserPayment(models.Model):
    user = models.ForeignKey(User, raw_id_admin=True)
    currency = models.CharField(max_length=3)
    amount = models.FloatField()
    euros = models.FloatField()
    paid = models.DateTimeField()

    class Admin:
        list_display = ('user', 'currency', 'amount', 'euros', 'paid')

    def __unicode__(self):
        return u'%s %.2f paid to %s on %s' % (
            self.currency, self.amount, self.user,
            self.paid.strftime('%Y-%m-%d'))


class NonProfit(models.Model):
    name = models.CharField(max_length=40)
    url = models.URLField()

    class Admin:
        list_display = ('name', 'url')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


class UserDonation(models.Model):
    user = models.ForeignKey(User, raw_id_admin=True)
    non_profit = models.ForeignKey(NonProfit)
    currency = models.CharField(max_length=3)
    amount = models.FloatField()
    euros = models.FloatField()
    donated = models.DateTimeField()

    class Admin:
        list_display = ('user', 'non_profit',
                        'currency', 'amount', 'euros', 'donated')

    def __unicode__(self):
        return u'%s %.2f donated to %s by %s on %s' % (
            self.currency, self.amount, self.non_profit, self.user,
            self.donated.strftime('%Y-%m-%d'))
