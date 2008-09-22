# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Helper functions for handling forms.
"""

__revision__ = "$Rev: 1464 $"
__date__ = "$Date: 2007-06-08 13:12:43 -0700 (Fri, 08 Jun 2007) $"
__author__ = "$Author: johann $"


def form_error(form):
    """
    Get a simple string for the first error in the form.
    """
    if not form.errors:
        return "No error."
    key = form.errors.keys()[0]
    error = unicode(form.errors[key][0])
    return "Invalid %s: %s" % (key, error)
