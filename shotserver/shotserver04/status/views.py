import socket
from django.db import connection
from django.template import RequestContext
from django.shortcuts import render_to_response
from shotserver04.websites.models import Website, Domain


def usage(http_request):
    cursor = connection.cursor()
    # Most frequently requested websites
    cursor.execute("""\
SELECT website_id, COUNT(*) AS groups
FROM requests_requestgroup
WHERE requests_requestgroup.submitted > NOW() - '24h'::interval
GROUP BY website_id
ORDER BY groups DESC
LIMIT 10
""")
    rows = cursor.fetchall()
    website_dict = Website.objects.in_bulk([row[0] for row in rows])
    website_list = [website_dict[row[0]] for row in rows]
    for index in range(len(website_list)):
        website_list[index].request_groups_per_day = rows[index][1]
    # Most frequently requested domains
    cursor.execute("""\
SELECT domain_id, COUNT(*) AS groups
FROM requests_requestgroup
JOIN websites_website ON (websites_website.id = website_id)
WHERE requests_requestgroup.submitted > NOW() - '24h'::interval
GROUP BY domain_id
ORDER BY groups DESC
LIMIT 10
""")
    rows = cursor.fetchall()
    domain_dict = Domain.objects.in_bulk([row[0] for row in rows])
    domain_list = [domain_dict[row[0]] for row in rows]
    for index in range(len(domain_list)):
        domain_list[index].request_groups_per_day = rows[index][1]
    # Most active IP addresses
    cursor.execute("""\
SELECT ip, COUNT(*) AS groups
FROM requests_requestgroup
WHERE requests_requestgroup.submitted > NOW() - '24h'::interval
GROUP BY ip
ORDER BY groups DESC
LIMIT 10
""")
    rows = cursor.fetchall()
    ip_list = [(row[0], socket.getfqdn(row[0]), row[1]) for row in rows]
    return render_to_response('status/usage.html', locals(),
        context_instance=RequestContext(http_request))
