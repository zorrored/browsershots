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
URLconf for the accounts app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.conf.urls.defaults import *
import django.contrib.auth.views as auth
from shotserver05.accounts import views

urlpatterns = patterns('accounts/',
    url(r'^create/$', views.create),
    url(r'^create/validate/(?P<field>\S+)/$', views.create_validate),
    url(r'^profile/$', views.profile),
    url(r'^login/$', auth.login,
        {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', auth.logout,
        {'template_name': 'accounts/logout.html'}),
    url(r'^password/change/$', auth.password_change,
        {'template_name': 'accounts/password_change_form.html'}),
    url(r'^password/change/done/$', auth.password_change_done,
        {'template_name': 'accounts/password_change_done.html'}),
    url(r'^password/reset/$', auth.password_reset,
        {'template_name': 'accounts/password_reset_form.html',
         'email_template_name': 'accounts/password_reset_email.html'}),
    url(r'^password/reset/done/$', auth.password_reset_done,
        {'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password/reset/confirm/(?P<uidb36>[^/]+)/(?P<token>[^/]+)/$',
        auth.password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'}),
    url(r'^password/reset/complete/$', auth.password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'}),
)
