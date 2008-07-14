#!/usr/bin/env python

import sys
import os
import socket
import httplib
import time

if len(sys.argv) == 2 and sys.argv[1] == '--spawn':
    for prefix in '0123456789abcdef':
        command = 'screen %s %s' % (sys.argv[0], prefix)
        print command
        result = os.system(command)
        if result:
            print 'failed with exit code', result
            sys.exit(result)
    sys.exit(0)

os.environ['DJANGO_SETTINGS_MODULE'] = 'shotserver04.settings'
from django.conf import settings
from shotserver04.screenshots import s3
from shotserver04.screenshots.models import Screenshot

server = s3.DEFAULT_HOST
aws = s3.AWSAuthConnection(
    settings.AWS_ACCESS_KEY_ID,
    settings.AWS_SECRET_ACCESS_KEY,
    is_secure=False,
    server=server)
s3_bucket = settings.S3_BUCKETS['original']


def debug_response(response):
    print 'common_prefixes', response.common_prefixes
    print 'name', response.name
    print 'marker', response.marker
    print 'prefix', response.prefix
    print 'is_truncated', response.is_truncated
    print 'delimiter', response.delimiter
    print 'max_keys', response.max_keys
    print 'next_marker', response.next_marker
    print 'entries'
    for entry in response.entries:
        print entry.key, entry.last_modified, entry.etag, entry.size
        print entry.storage_class, entry.owner


def find_existing_hashkeys(response):
    hashkeys = [entry.key[:32] for entry in response.entries]
    existing = Screenshot.objects.filter(hashkey__in=hashkeys)
    return [screenshot.hashkey for screenshot in existing]


def delete_entry(key):
    for name, bucket in settings.S3_BUCKETS.iteritems():
        for attempt in range(3):
            try:
                status = aws.delete(bucket, key).http_response.status
                print status,
                if status == 204:
                    break
            except httplib.BadStatusLine:
                print 'H',
            except socket.error:
                print 'S',
            time.sleep(1)


options = {'marker': ''}
if len(sys.argv) > 1:
    options['prefix'] = sys.argv[1]
if len(sys.argv) > 2:
    options['marker'] = sys.argv[2]
for run in range(1, 1001):
    print 'run', run
    response = aws.list_bucket(s3_bucket, options)
    if len(response.entries) == 0:
        break
    for entry in response.entries:
        print entry.last_modified, entry.key, entry.size,
        if entry.last_modified < '2008-05-15':
            delete_entry(entry.key)
            print 'deleted'
        else:
            print 'kept'
    options['marker'] = response.entries[-1].key
