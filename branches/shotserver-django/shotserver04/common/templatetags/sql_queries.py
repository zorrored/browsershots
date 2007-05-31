from django import template
from django.db import connection

register = template.Library()

TABLE_TEMPLATE = """
<table id="sqldebug">
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
        _("Time"),
        _("Database queries"),
        '\n'.join(rows),
        )
