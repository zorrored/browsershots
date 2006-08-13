#! /usr/bin/python

import sys, os, re, time

split = re.compile(r'(.+/(\d\d\d\d)/(\d\d)/(\d\d)/([^/]+))/content$').match
for filename in sys.stdin:
    match = split(filename)
    if match is None:
        continue
    path, dyear, dmonth, dday, entry = match.groups()

    title = file(path + '/title').readline().strip()
    categories = ''.join(file(path + '/categories').readlines()).split()
    category = categories[0]

    published = int(float(file(path + '/published').readline().strip()))
    localtime = time.localtime(published)
    year, month, day, hour, minute, second, wday, yday, isdst = localtime
    if hour == 23 and minute == 0 and second == 0:
        published += 3600
        localtime = time.localtime(published)
        year, month, day, hour, minute, second, wday, yday, isdst = localtime
    offset = isdst + 1

    date = '%04u-%02u-%02uT%02u:%02u:%02uZ' % (
        year, month, day, hour, minute, second)

    content = ''.join(file(path + '/content').readlines()).rstrip()

    outdir = 'entries/' + category
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outfilename = '%s/%s.txt' % (outdir, entry)
    print outfilename, date

    outfile = file(outfilename, 'w')
    outfile.write(title + '\n')
    outfile.write('#date ' + date + '\n')
    outfile.write(content + '\n')
    outfile.close()
