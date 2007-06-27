# browsershots.org - Test your web design in different browsers
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
XML-RPC interface for factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver04.common import get_or_fault
from shotserver04.xmlrpc import register
from shotserver04.factories.models import Factory
from shotserver04.requests.models import Request


@register(str, str)
def features(http_request, factory_name):
    """
    Generate SQL WHERE clause to match requests for this factory.

    Arguments
    ~~~~~~~~~
    * factory_name string (lowercase, normally from hostname)

    Return value
    ~~~~~~~~~~~~
    * where string (SQL WHERE clause)
    """
    factory = get_or_fault(Factory, name=factory_name)
    joins, where, params = factory.features_q().get_sql(Request._meta)
    where = ' AND '.join(where)
    return where % tuple(params)
