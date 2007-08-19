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
Display project sponsor logos with links.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from shotserver03.interface import xhtml


def write():
    """
    Write XHTML div with sponsor logos.
    """
    xhtml.write_open_tag_line('div', _id="sponsors")
    xhtml.write_tag_line('h2', "Sponsors")

    img = xhtml.tag('img', src="/style/mfg40.png",
                    alt="MFG Stiftung BW", _class="top")
    link = xhtml.tag('a', img, href="http://www.mfg.de/stiftung/")
    xhtml.write_tag_line('p', link)

    img = xhtml.tag('img', src="/style/lisog40.png",
                    alt="LiSoG e.V.", _class="top")
    link = xhtml.tag('a', img, href="http://www.lisog.org/")
    xhtml.write_tag_line('p', link)

    img = xhtml.tag('img', src="/style/topalis40.png",
                    alt="Topalis AG", _class="top")
    link = xhtml.tag('a', img, href="http://www.topalis.com/")
    xhtml.write_tag_line('p', link)

    img = xhtml.tag('img', src="/style/brandup40.png",
                    alt="Brand Up LLC", _class="top")
    link = xhtml.tag('a', img, href=
"http://brand-up.com/?utm_source=Browsershots&amp;utm_medium=sponsorship")
    xhtml.write_tag_line('p', link)

    xhtml.write_close_tag_line('div') # id="sponsors"
