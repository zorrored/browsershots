"""
pubdate.py
Copyright 2006 Johann C. Rocholl <johann@rocholl.net>

Inspired by the unmaintained metadate plugin (Error 403 for
http://www.binaryuprising.com/code/pyblosxom/metadate.py on
2006-08-12).

If a file contains a line like the following below the title line,
this plugin changes the mtime to be the timestamp instead of the one
kept by the filesystem:

#pubDate Tue, 07 Jun 2005 00:00:00 +0200

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os, re, time

months = ["0",
          "Jan", "Feb", "Mar", "Apr",
          "May", "Jun", "Jul", "Aug",
          "Sep", "Oct", "Nov", "Dec"]

wdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

timestamp_match = re.compile(r'#pubDate\s+' +
                             r'(|\w{3},)\s*' +
                             r'(\d{2})\s+(\w{3})\s+(\d{4})\s+' +
                             r'(\d{2}):(\d{2}):(\d{2})\s+' +
                             r'([+\-]\d{2})(\d{2})').match

def cb_filestat(args):
    filename = line = '(unset)'
    try:
        filename = args["filename"]
        infile = file(filename)
        title = infile.readline()
        while True:
            line = infile.readline()
            if not line.startswith('#'):
                break
            match = timestamp_match(line)
            if match:
                day = int(match.group(2))
                month = months.index(match.group(3))
                year = int(match.group(4))
                hour = int(match.group(5))
                minute = int(match.group(6))
                second = int(match.group(7))
                offset_hour = int(match.group(8))
                offset_minute = int(match.group(9))

                dst = -1
                # dst = offset_hour == 2
                timetuple = (year, month, day,
                             hour, minute, second,
                             0, 0, dst)
                unixtime =  time.mktime(timetuple)

                mtime = list(args["mtime"])
                mtime[8] = unixtime
                args["mtime"] = tuple(mtime)
    except:
        # TODO: Some sort of debugging code here?
        print filename, line
        raise
    return args
