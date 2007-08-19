# browsershots.org ShotServer 0.3-beta1
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
Database interface for lock table.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

# How long may a factory work on a screenshot request?
lock_timeout = '0:03:00'

# How long will a failed screenshot be blocked from a factory?
failure_timeout = '0:10:00'

# How tall can a screenshot be, in pixels?
max_screenshot_height = 8000
