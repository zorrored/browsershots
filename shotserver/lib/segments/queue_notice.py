# browsershots.org
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
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
Show a message about queue length.
"""

__revision__ = '$Rev$'
__date__ = '$Date$'
__author__ = '$Author$'

from shotserver03.interface import xhtml

def write():
    """
    Write XHTML paragraph about queue length.
    """
    queue_link = xhtml.tag('a', 'queue', href="http://v03.browsershots.org/queue/")
    xhtml.write_open_tag('p', _id="queue-notice")
    req.write('\n'.join((
        "<b>Important notice:</b> The %s is quite full at the moment." % queue_link,
        "Some of your screenshot requests will expire before they can be processed.",
        "See the <b>maximum wait</b> option at the bottom of this page.",
        "Please try again in a few days.",
        xhtml.tag('a', "I'm looking for volunteers to run more screenshot factories.",
                  href="http://trac.browsershots.org/wiki/HowToCreateNewShotFactory"),
        )))
    xhtml.write_close_tag_line('p') # id="queue-notice"
