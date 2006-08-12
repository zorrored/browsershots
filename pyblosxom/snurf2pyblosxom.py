#! /usr/bin/python

import sys, os, re, time

months = ["0",
          "Jan", "Feb", "Mar", "Apr",
          "May", "Jun", "Jul", "Aug",
          "Sep", "Oct", "Nov", "Dec"]

wdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

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

    pubdate = '%s, %02u %s %04u %02u:%02u:%02u +%02u00' % (
        wdays[wday], day, months[month], year, hour, minute, second, offset)

    content = ''.join(file(path + '/content').readlines()).rstrip()

    outdir = 'entries/' + category
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    outfilename = '%s/%s.txt' % (outdir, entry)
    print outfilename, pubdate

    outfile = file(outfilename, 'w')
    outfile.write(title + '\n')
    outfile.write('#pubDate ' + pubdate + '\n')
    outfile.write(content + '\n')
    outfile.close()
