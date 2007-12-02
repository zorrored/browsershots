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
Count screenshots per factory admin during the last month.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import sys
LAST_MONTH_REVENUE = float(sys.argv[1])

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'

from datetime import datetime, timedelta
from shotserver04.factories.models import Factory
from shotserver04.screenshots.models import Screenshot

now = datetime.now()
if now.month > 1:
    start = datetime(now.year, now.month - 1, 1, 0, 0, 0)
else:
    start = datetime(now.year - 1, 12, 1, 0, 0, 0)
stop = datetime(now.year, now.month, 1, 0, 0, 0)
print start, 'until', stop, '(%s)' % (stop - start)

admins = {}
admin_uploads = {}
factory_uploads = {}

total = Screenshot.objects.filter(
    uploaded__gte=start, uploaded__lt=stop).count()

# Count uploads in the last month for factories and admins
factories_total = 0
factories = Factory.objects.filter(last_upload__gte=start)
for factory in factories:
    uploads = factory.screenshot_set.filter(
        uploaded__gte=start, uploaded__lt=stop).count()
    # print uploads, factory
    if not factory.admin_id in admin_uploads:
        admin_uploads[factory.admin_id] = 0
    factory_uploads[factory.id] = uploads
    admin_uploads[factory.admin_id] += uploads
    admins[factory.admin_id] = factory.admin
    factories_total += uploads
print total, factories_total, 'total'
total = factories_total

admin_ids = admin_uploads.keys()
admin_ids.sort(key=lambda admin_id: -admin_uploads[admin_id])
for admin_id in admin_ids:
    print admin_uploads[admin_id], admins[admin_id],
    print '%.1f%%' % (100.0 * admin_uploads[admin_id] / total),
    print '%.2f EUR' % (LAST_MONTH_REVENUE * admin_uploads[admin_id] / total)
    admin_factories = [f for f in factories
                       if f.admin_id == admin_id
                       and factory_uploads[f.id]]
    if len(admin_factories) > 1:
        admin_factories.sort(key=lambda f: -factory_uploads[f.id])
        for factory in admin_factories:
            print '   ', factory_uploads[factory.id], factory
