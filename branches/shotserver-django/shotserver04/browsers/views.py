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
Browser views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms
from django.shortcuts import render_to_response, get_object_or_404
from shotserver04 import settings
from shotserver04.common import lazy_gettext_capfirst as _
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.browsers import agents


class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput)


BrowserForm = forms.form_for_model(Browser)


def add_browser(http_request):
    # Use lazy translation for field labels
    for key in BrowserForm.base_fields:
        BrowserForm.base_fields[key].label = _(
            Browser._meta.get_field(key).verbose_name)
    # Prefill form fields with user agent from HTTP request
    user_agent = http_request.META['HTTP_USER_AGENT']
    initial = {
        'user_agent': user_agent,
        'javascript': 2, # enabled
        'java': 2, # enabled
        'flash': 2, # enabled
        }
    # Guess factory name from IP address
    factories = Factory.objects.filter(
        ip=http_request.META['REMOTE_ADDR'])[:1]
    if not factories:
        factories = Factory.objects.all()[:1]
    if factories:
        initial['factory'] = factories[0].id
    # Extract engine and engine version from user agent string
    for engine in agents.get_engines():
        if engine.name in user_agent:
            initial['engine'] = engine.id
            initial['engine_version'] = agents.extract_version(
                user_agent, engine.name)
            break
    # Extract browser group and version from user agent string
    for browser_group in agents.get_browser_groups():
        if browser_group.name in user_agent:
            initial['browser_group'] = browser_group.id
            version = agents.extract_version(
                user_agent, browser_group.name)
            initial['version'] = version
            initial['major'] = agents.extract_major(version)
            initial['minor'] = agents.extract_minor(version)
            break
    form = BrowserForm(http_request.POST or initial)
    password_form = PasswordForm()
    field_groups = [[
        [form['user_agent']],
        [form['command']],
        ], [
        [form['browser_group'], form['version'], form['major'], form['minor']],
        [form['engine'], form['engine_version']],
        ], [
        [form['javascript'], form['java'], form['flash']],
        ], [
        [form['factory']],
        [password_form['password']],
        ]]
    admin_email = '<a href="mailto:%s">%s</a>' % (
        settings.ADMINS[0][1], settings.ADMINS[0][0])
    return render_to_response('browsers/add_browser.html', locals())
