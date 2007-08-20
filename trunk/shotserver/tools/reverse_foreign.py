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
Reverse foreign keys from one table to the other.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

screenshots = file('screenshots_screenshot.sql').readlines()
screenshots.pop(0)
screenshots.pop(-1)

requests = file('requests_request.sql').readlines()
print requests.pop(0).rstrip('\n').replace('uploaded', 'screenshot_id')
end = requests.pop(-1).rstrip('\n')


def find_screenshot(request_id):
    for screenshot in screenshots:
        values = screenshot.rstrip('\n').split('\t')
        if values[2] == request_id:
            return values[0]
    return r'\N'


for request in requests:
    values = request.rstrip('\n').split('\t')
    uploaded = values[-1]
    values = values[:-1] + [find_screenshot(values[0])]
    print '\t'.join(values)

print end
