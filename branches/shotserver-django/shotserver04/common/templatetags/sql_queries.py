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
from django.utils.text import capfirst

register = template.Library()

JAVASCRIPT = u"""
document.getElementById('sql-queries').style.display='block';
""".strip()

LINK_TEMPLATE = u"""
<a href="%s" onclick="%s" name="sql">%s</a>
""".strip()

TABLE_TEMPLATE = u"""
<table class="debug" id="sql-queries" style="display:none">
%s
</table>
""".strip()


@register.simple_tag
def sql_link():
    """
    Display an HTML link to display the queries table.
    """
    if not connection.queries:
        return ''
    caption = capfirst(_(u"%(count)d database queries")) % {
        'count': len(connection.queries)}
    return LINK_TEMPLATE % ('#sql', JAVASCRIPT, caption)


@register.simple_tag
def sql_queries():
    """
    Display an HTML table with all SQL queries for this HTTP request.
    """
    if not connection.queries:
        return ''
    rows = []
    for index, query in enumerate(connection.queries):
        rows.append(u'<tr class="%s"><td>%s</td><td>%s</td></tr>' % (
            'row%d' % (index % 2 + 1),
            query['time'],
            query['sql'].replace('","', '", "'),
            ))
    return TABLE_TEMPLATE % '\n'.join(rows)
