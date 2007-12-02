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
REVENUE = float(sys.argv[1])

users = {}
for line in file('auth_user.sql'):
    parts = line.split('\t')
    if not parts or not parts[0].isdigit():
        continue
    user_id = int(parts[0])
    username = parts[1]
    first_name = parts[2]
    last_name = parts[3]
    email = parts[4]
    users[user_id] = (username, first_name, last_name, email)

factories = {}
for line in file('factories_factory.sql'):
    parts = line.split('\t')
    if not parts or not parts[0].isdigit():
        continue
    factory_id = int(parts[0])
    name = parts[1]
    admin_id = int(parts[2])
    factories[factory_id] = (name, admin_id)

total = 0
admin_uploads = {}
factory_uploads = {}
for line in file('screenshots_screenshot.sql'):
    parts = line.split('\t')
    if not parts or not parts[0].isdigit():
        continue
    screenshot_id = int(parts[0])
    factory_id = int(parts[3])
    factory_uploads[factory_id] = factory_uploads.get(factory_id, 0) + 1
    if factory_id not in factories:
        print 'WARNING: unknown factory', factory_id
        continue
    admin_id = factories[factory_id][1]
    if admin_id not in users:
        print 'WARNING: unknown user', admin_id
    admin_uploads[admin_id] = admin_uploads.get(admin_id, 0) + 1
    total += 1

print total, 'total'

admin_ids = admin_uploads.keys()
admin_ids.sort(key=lambda admin_id: -admin_uploads[admin_id])
for admin_id in admin_ids:
    admin = users[admin_id]
    print admin_uploads[admin_id],
    print '%.1f%%' % (100.0 * admin_uploads[admin_id] / total),
    print '%.2f' % (REVENUE * admin_uploads[admin_id] / total),
    print ' '.join(admin)
    admin_factories = [factory_id
                       for factory_id in factories
                       if factories[factory_id][1] == admin_id
                       and factory_id in factory_uploads
                       and factory_uploads[factory_id]]
    if len(admin_factories) > 1:
        admin_factories.sort(
            key=lambda factory_id: -factory_uploads[factory_id])
        for factory_id in admin_factories:
            print '   ', factory_uploads[factory_id],
            print factories[factory_id][0]
