#!/usr/bin/env python

import sys
import re

min_date = sys.argv[-1]
date_search = re.compile(r'(20\d\d-\d\d-\d\d)').search
assert date_search(min_date) is not None

for line in sys.stdin:
    line = line.rstrip()
    match = date_search(line)
    if match is not None:
        date = match.group(1)
        if date < min_date:
            continue
    print line
