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
Show a message about queue length.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml


def write():
    """
    Write XHTML paragraph about queue length.
    """
    queue_link = xhtml.tag('a', '%s',
        href="http://v03.browsershots.org/queue/")
    wiki_link = xhtml.tag('a', '%s',
        href="http://trac.browsershots.org/wiki/HowToCreateNewShotFactory")
    xhtml.write_open_tag('p', _id="queue-notice")
    req.write('\n'.join((
"<b>%s</b>" % "Important notice:",
queue_link % "The queue is quite full at the moment.",
"Some of your screenshot requests will expire before they can be processed.",
"Please try again in a few days.",
"I'm looking for volunteers to run more screenshot factories.",
wiki_link % "If you want to help, see the wiki for more information.")))
    xhtml.write_close_tag_line('p') # id="queue-notice"
