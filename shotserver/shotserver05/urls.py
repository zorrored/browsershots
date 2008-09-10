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
Main URLconf for shotserver05.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import os
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^factories/', include('shotserver05.factories.urls')),
    (r'^users/', include('shotserver05.users.urls')),
    (r'^xmlrpc/', include('shotserver05.xmlrpc.urls')),
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    # Serve CSS and image files from shotserver04/static/
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.join(os.path.normpath(
                        os.path.dirname(__file__)), 'static')}),
#        (r'^png/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': settings.PNG_ROOT}),
        )
