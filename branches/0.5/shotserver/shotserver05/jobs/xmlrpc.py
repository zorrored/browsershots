# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
XML-RPC methods for the jobs app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import xmlrpclib
from shotserver05.xmlrpc.utils import factory_auth
from shotserver05.factories.utils import jobs_for_factory
from shotserver05.jobs.utils import browser_for_job
from shotserver05.screenshots.models import Attempt


@factory_auth
def poll(factory):
    """
    Arguments:
    ~~~~~~~~~~
    * factory_name string (lowercase)

    Return value:
    ~~~~~~~~~~~~~
    * job dict (if matching job found)

    The job dict will contain the following keys:

    * hashkey string
    * browser string
    * major int
    * minor int
    * command string
    """
    jobs = jobs_for_factory(factory)[:1]
    if not len(jobs):
        raise xmlrpclib.Fault(204, "No matching requests.")
    job = jobs[0]
    browser = browser_for_job(job, factory)
    attempt = Attempt.objects.create(job=job, factory=factory)
    return {
        'hashkey': attempt.hashkey,
        'browser': job.group.slug,
        'version': browser.version,
        'major': browser.major,
        'minor': browser.minor,
        'command': browser.command,
        }
