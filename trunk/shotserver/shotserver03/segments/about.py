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
Explain the purpose of this project.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml


def write():
    """
    Write XHTML div with a quick project introduction.
    """
    xhtml.write_open_tag_line('div', _id="about")
    xhtml.write_tag_line('h2', "What is this?")

    text = '\n'.join((
"Browsershots makes screenshots of your web design in different browsers.",
"It is a free open-source online service created by Johann C. Rocholl.",
"When you submit your web address, it will be added to the job queue.",
"A number of distributed computers will open your website in their browser.",
"Then they will make screenshots and upload them to the central server here.",
))
    xhtml.write_tag_line('p', text)

    xhtml.write_close_tag_line('div') # id="about"
