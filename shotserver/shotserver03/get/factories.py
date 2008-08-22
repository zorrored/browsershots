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
List all factories.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
from shotserver03.interface import xhtml
from shotserver03.segments import factory_list
from shotserver03.segments import factory_info, factory_browsers, screenshots
from shotserver03 import database


def read_params():
    """
    Read parameters from the request URL.
    """
    database.connect()
    try:
        if len(req.info.options) == 0:
            req.params.show_factories = database.factory.select_active()
        else:
            factory = req.info.options[0]
            if factory.isdigit():
                req.params.factory = factory
                req.params.factory_name = \
                    database.factory.serial_to_name(factory)
            else:
                req.params.factory_name = factory
                req.params.factory = database.factory.name_to_serial(factory)
            req.params.show_screenshots = database.screenshot.select_recent(
                'screenshot.factory = %s', (req.params.factory, ))
    finally:
        database.disconnect()


def title():
    """Return page title."""
    if hasattr(req.params, 'factory'):
        return "Screenshot Factory: %s" % req.params.factory_name
    else:
        return "Screenshot Factories"


def write_img(name):
    """Show factory image."""
    src = '/static/factories/240/%s.jpg' % name
    if os.path.exists('/var/www/browsershots.org' + src):
        alt = "Picture of screenshot factory %s." % name
        img = xhtml.tag('img', src=src, alt=alt)
        xhtml.write_tag_line('p', img, _class="float-right")


def body():
    """
    Write HTML page content.
    """
    if hasattr(req.params, 'factory'):
        write_img(req.params.factory_name)
        xhtml.write_tag_line('p',
            "This page shows the configuration of the screenshot factory %s."
            % xhtml.tag('b', req.params.factory_name))
        factory_info.write()
        xhtml.write_tag_line('hr')
        xhtml.write_tag_line('h2', 'Installed Browsers')
        factory_browsers.write()
        if req.params.show_screenshots:
            xhtml.write_tag_line('hr')
            xhtml.write_tag_line('h2', 'Recent screenshots')
            screenshots.write()
    else:
        factory_list.write()
