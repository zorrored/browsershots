#!/usr/bin/env python
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
Count screenshots per factory per day.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'

import sys
from django.contrib.auth.models import User
from shotserver04.factories.models import Factory
from shotserver04.revenue.models import FactoryScreenshotCount


def save_factory(factory, date, screenshots):
    if screenshots:
        count, created = FactoryScreenshotCount.objects.get_or_create(
            factory=factory, date=date, defaults={'screenshots': screenshots})
        if not created and count.screenshots != screenshots:
            count.update_fields(screenshots=screenshots)
    else:
        FactoryScreenshotCount.objects.filter(
            factory=factory, date=date).delete()


def save(date, factory_uploads):
    save_factory(None, date, factory_uploads.get(None, 0))
    for factory in Factory.objects.all():
        save_factory(factory, date, factory_uploads.get(factory.id, 0))


previous_date = None
factory_uploads = {}
for line in sys.stdin:
    parts = line.split('\t')
    if not parts or not parts[0].isdigit():
        continue
    factory_id = int(parts[3])
    date, time = parts[7].split()
    if previous_date and date != previous_date:
        save(previous_date, factory_uploads)
        factory_uploads = {}
    previous_date = date
    factory_uploads[factory_id] = factory_uploads.get(factory_id, 0) + 1
    factory_uploads[None] = factory_uploads.get(None, 0) + 1
save(previous_date, factory_uploads)
