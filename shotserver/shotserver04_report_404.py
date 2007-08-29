#!/usr/bin/env python

import sys
import re
import socket

MAX_EXAMPLES = 5
ORPHANS = 3
INDENT = ' ' * 3

log_match = re.compile(r"""
(?P<ip>\d+\.\d+\.\d+\.\d+)\s
(\S+)\s
(\S+)\s
\[
(?P<day>\d+)/(?P<month>\w+)/(?P<year>\d+):
(?P<hour>\d+):(?P<min>\d+):(?P<sec>\d+)\s
(?P<timezone>[+-]\d+)
\]\s
"(?P<method>\w+)\s(?P<path>.+?)\s(?P<protocol>\S+)"\s
(?P<status>\d+)\s
(?P<size>\S+)\s
"(?P<referer>.+?)"\s
"(?P<useragent>.+?)"\s
""", re.VERBOSE).match


def categorize(matches, key, max_examples=MAX_EXAMPLES):
    categories = {}
    for match in matches:
        value = match.group(key)
        categories[value] = categories.get(value, 0) + 1
    counts = [(count, category) for category, count in categories.iteritems()]
    counts.sort()
    counts.reverse()
    if key == 'path':
        print '=' * (61 + len(INDENT))
    elif len(counts) > 1:
        print INDENT, '-' * 60
    stop = min(len(counts), max_examples)
    if stop + ORPHANS >= len(counts):
        stop = len(counts)
    for index in range(stop):
        count, category = counts[index]
        if key == 'ip':
            category += ' (%s)' % socket.getfqdn(category)
        if count == len(matches):
            count = 'all'
        print INDENT, count, 'from', key, category
    if stop < len(counts):
        rest = sum([count[0] for count in counts[stop:]])
        print INDENT, rest, 'from', len(counts) - stop, 'other', key + 's'


def error_details(matches):
    categorize(matches, 'path', max_examples=10)
    categorize(matches, 'ip')
    categorize(matches, 'referer')
    categorize(matches, 'useragent')


# Collect all errors by first part of URL path.
errors = {}
for line in sys.stdin:
    match = log_match(line)
    if match is None:
        continue
    if match.group('status')[0] in '23':
        continue
    firstpart = match.group('path').lstrip('/').split('/')[0]
    if firstpart not in errors:
        errors[firstpart] = []
    errors[firstpart].append(match)

# Count errors and sort by number of occurrences
counts = []
for firstpart in errors:
    counts.append((len(errors[firstpart]), firstpart))
counts.sort()
counts.reverse()

# Print errors, most common first, with supporting info
for count, firstpart in counts:
    print count, 'errors for /%s' % firstpart
    error_details(errors[firstpart])
    print
