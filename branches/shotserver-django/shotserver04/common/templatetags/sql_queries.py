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
Show a table with SQL queries for the current HTTP request, for
debugging and optimizing.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import template
from django.db import connection

register = template.Library()

JAVASCRIPT = """
document.getElementById('sql-queries').style.display='block';
""".strip()

TABLE_TEMPLATE = """
<p class="debug"><a onclick="%s" href="#sql" name="sql">%s</a></p>
<table class="debug" id="sql-queries" style="display:none">
<thead>
<tr><th>%s</th><th>%s</th></tr>
</thead>
<tbody>
%s
</tbody>
</table>
""".strip()


@register.simple_tag
def sql_queries():
    if not connection.queries:
        return ''
    rows = []
    for index, query in enumerate(connection.queries):
        rows.append('<tr class="%s"><td>%s</td><td>%s</td></tr>' % (
            'row%d' % (index % 2 + 1),
            query['time'],
            query['sql'].replace('","', '", "'),
            ))
    return TABLE_TEMPLATE % (
        JAVASCRIPT,
        _("Database queries"),
        _("Time"),
        _("Database queries"),
        '\n'.join(rows),
        )
