# browsershots.org - Test your web design in different browsers
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
Global URL configuration.

This dispatches to the configuration for each installed app according
to the first part of the request URL.

URLs of the form http://browsershots.org/http://www.example.com/
will be handled by the websites app.

If settings.DEBUG is enabled (typically when the development server is
running), URLs starting with /static/ or /png/ will be handled by
Django, otherwise you should include them in the Apache configuration.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.conf.urls.defaults import patterns, include
from shotserver04 import settings


def load_app_patterns(prefix, ignore=()):
    """
    Include URL configuration for installed apps.
    """
    pairs = []
    for app in settings.INSTALLED_APPS:
        if app.startswith(prefix):
            segment = app.split('.')[-1]
            if segment not in ignore:
                pairs.append((r'^%s/' % segment, include(app + '.urls')))
    return pairs


urlpatterns = patterns('',
    (r'^$', 'shotserver04.common.views.start'),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^i18n/', include('django.conf.urls.i18n')),
    (r'^(?P<website_url>https?://\S+)$',
         'shotserver04.websites.views.website_detail'),
    *load_app_patterns('shotserver04.', ignore=['common']))


def get_static_path():
    """Get path to static CSS, Javascript, image files."""
    import os
    return os.path.join(os.path.normpath(os.path.dirname(__file__)), 'static')


if settings.DEBUG:
    # Serve CSS and image files from shotserver04/static/
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': get_static_path()}),
        (r'^png/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.PNG_ROOT}),
        )
