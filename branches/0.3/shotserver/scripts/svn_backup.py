#!/usr/bin/env python
# browsershots.org ShotServer 0.3-beta1
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
usage: svn_backup.py [--full] <repos_path> <backup_dir>

Backup a Subversion repository. Will create a file with a name like
  <backup_dir>/<repos_name>-r0-r212.dump.bz2
where <repos_name> is the last part of <repos_path> and 0 and 212 are
the first and last revisions in the backup file.

The <backup_dir> can be the same for all your repositories, if your
<repos_name>s are unique. Otherwise, use different <backup_dir>s.

When called with --full, the first revision will be zero. Otherwise,
the names of existing files in the backup dir are scanned for the
maximum revision that has been backed up already. First is then set to
the maximum + 1, e.g. 213 if the example file above is found. The dump
is then performed with --incremental and will contain only changed
files in new revisions since the last backup.

The last revision number is retrieved directly from the repository.

Recommended use: for each of your repositories call
"svn_backup.py <repository> <backup_dir>" from a daily cronjob and
"svn_backup.py --full <repository> <backup_dir>" from a weekly one.
Then use rsync and a CD burner to backup the <backup_dir> every month.

For best results, make sure that your <backup_dir> is on a different
machine (NTFS or SMB). If this is not possible, use a different hard
drive. If this is not possible, use a different partition. If this is
not possible, you'll be screwed. Oh, and don't use a RAM disk either.
"""

__revision__ = '$Rev: 706 $'
__date__ = '$Date: 2005-08-21 09:37:54 +0200 (Sun, 21 Aug 2005) $'
__author__ = '$Author: johann $'

import os
import sys
import glob
import re


def system(command, debug = False):
    """
    Run a shell command.
    """
    if debug:
        print command
    err = os.system(command)
    if err:
        raise RuntimeError("%s failed with exit code %d" % (command, err))


def backticks(command):
    """
    Run a shell command and return its output as a string.
    """
    child = os.popen(command)
    output = child.read()
    err = child.close()
    if err:
        raise RuntimeError("%s failed with exit code %d" % (command, err))
    return output


def find_latest(backup, basename):
    """
    Find the latest backup revision.
    """
    latest = -1
    pattern = "%s/%s-r*-r*.dump.bz2" % (backup, basename)
    re_revisions = re.compile(r"-r\d+-r(\d+)\.dump\.bz2$")
    for filename in glob.glob(pattern):
        match = re_revisions.search(filename)
        if match:
            last = int(match.group(1))
            if last > latest:
                latest = last
    return latest


def usage(message = None):
    """
    Print a usage line (and possibly an error message) and exit with
    return code 1.
    """
    print "usage: %s [--full] <repos_path> <backup_dir>" % (
        os.path.basename(sys.argv[0]))
    if message:
        print "error:", message
    sys.exit(1)


def read_options():
    """
    Read options from command line.
    """
    full = False
    # Parse options.
    while len(sys.argv) > 1 and sys.argv[1].startswith("-"):
        option = sys.argv.pop(1)
        if option == "--full":
            full = True
        else:
            usage("unknown option %s" % option)
    if len(sys.argv) != 3:
        usage()
    # Normalize path name arguments.
    dummy, repos, backup = sys.argv
    while repos.endswith("/"):
        repos = repos[:-1]
    while backup.endswith("/"):
        backup = backup[:-1]
    return full, repos, backup


def find_backup_range(full, repos, backup, basename):
    """
    Find start and stop revision numbers.
    """
    already = find_latest(backup, basename)
    start = already + 1
    stop = int(backticks("svnlook youngest %s" % repos).strip())
    if full:
        start = 0
    return start, stop


def run_backup():
    """
    Run a subversion backup.
    """
    full, repos, backup = read_options()
    basename = os.path.basename(repos)
    start, stop = find_backup_range(full, repos, backup, basename)
    if start > stop:
        return # nothing to do

    # move older version of same file out of the way
    date = backticks("date +%Y-%m-%d").strip()
    outfile = "%s/%s-r%u-r%u.dump.bz2" % (backup, basename, start, stop)
    oldfile = "%s/%s-r%u-r%u.%s.dump.bz2" % (
        backup, basename, start, stop, date)
    if os.path.exists(outfile):
        system("mv %s %s" % (outfile, oldfile))

    # build and run subversion backup command
    parts = []
    parts.append("svnadmin dump --quiet")
    if not full:
        parts.append("--incremental")
    parts.append("--revision %u:%u %s" % (start, stop, repos))
    parts.append("| bzip2 > %s" % outfile)
    system(' '.join(parts))

    # compare and delete old version of same file
    if os.path.exists(oldfile):
        different = os.system("cmp %s %s" % (outfile, oldfile))
        if not different:
            system("rm -f %s" % oldfile)


if __name__ == '__main__':
    run_backup()
