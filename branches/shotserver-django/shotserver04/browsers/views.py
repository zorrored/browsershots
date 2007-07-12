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
from django.db import connection
from django.http import HttpResponseRedirect
from django import newforms as forms
from django.newforms.util import ErrorList
from django.contrib.auth.models import check_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from shotserver04 import settings
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser
from shotserver04.browsers import agents


class PasswordForm(forms.Form):
    """
    Simple password input form.
    """
    password = forms.CharField(
        label=_('password'),
        widget=forms.PasswordInput)


BrowserForm = forms.form_for_model(Browser)


def guess_factory(ip, user_agent, name=None):
    """
    Guess factory name from IP address and User-Agent, or optionally
    from factory parameter in query string.
    """
    if name:
        factories = Factory.objects.select_related().filter(name=name)
        if len(factories):
            return factories[0]
    factories = Factory.objects.select_related().filter(ip=ip)
    if not factories:
        factories = Factory.objects.select_related()
    # Try to match Ubuntu or Mac OS X
    for factory in factories:
        if factory.operating_system.name in user_agent:
            return factory
    # Try to match Linux or Windows
    for factory in factories:
        if factory.operating_system.platform.name in user_agent:
            return factory
    # Try to match PPC or i686
    for factory in factories:
        if factory.architecture.name in user_agent:
            return factory
    if factories:
        return factories[0]


def add(http_request):
    """
    Add a browser that is installed on a screenshot factory.
    """
    # Use lazy translation for field labels
    for key in BrowserForm.base_fields:
        BrowserForm.base_fields[key].label = _(
            Browser._meta.get_field(key).verbose_name)
    # Prefill form fields with user agent from HTTP request
    user_agent = http_request.META['HTTP_USER_AGENT']
    initial = {
        'user_agent': user_agent,
        'javascript': 1, # disabled
        'java': 1, # disabled
        'flash': 1, # disbled
        }
    # Guess factory name from IP address
    ip = http_request.META['REMOTE_ADDR']
    factory = guess_factory(ip, user_agent,
        http_request.GET.get('factory', None))
    if factory:
        initial['factory'] = factory.id
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
            initial['major'] = agents.extract_major(
                version, browser_group.name)
            initial['minor'] = agents.extract_minor(
                version, browser_group.name)
            break
    form = BrowserForm(http_request.POST or initial)
    password_form = PasswordForm(http_request.POST or None)
    password_form['password'].field.widget.render_value = False
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
    admin_email = u'<a href="mailto:%s">%s</a>' % (
        settings.ADMINS[0][1], settings.ADMINS[0][0])
    password_valid = False
    if form.is_valid() and password_form.is_valid():
        if password_form.cleaned_data['password']:
            password_valid = check_password(
                password_form.cleaned_data['password'],
                form.cleaned_data['factory'].admin.password)
            if not password_valid:
                password_form.errors['password'] = ErrorList(
                    [_("Password mismatch.")])
    if not password_valid:
        return render_to_response('browsers/add.html', locals())
    cursor = connection.cursor()
    where = u"""((factory_id = %s AND user_agent = %s) OR
(factory_id = %s AND browser_group_id = %s AND major = %s AND minor = %s))"""
    params = [
        form.cleaned_data['factory'].id,
        form.cleaned_data['user_agent'],
        form.cleaned_data['factory'].id,
        form.cleaned_data['browser_group'].id,
        form.cleaned_data['major'],
        form.cleaned_data['minor'],
        ]
    # Delete old unused versions of the same browsers
    cursor.execute("""
DELETE FROM browsers_browser
WHERE """ + where + """
AND NOT EXISTS(SELECT 1 FROM screenshots_screenshot
               WHERE browser_id = browsers_browser.id LIMIT 1)
AND NOT EXISTS(SELECT 1 FROM requests_request
               WHERE browser_id = browsers_browser.id LIMIT 1)
""", params)
    # Deactivate old versions of the same browser
    cursor.execute("""
UPDATE browsers_browser SET active = FALSE
WHERE """ + where, params)
    # Create new browser with submitted data
    form.cleaned_data['active'] = True
    Browser.objects.create(**form.cleaned_data)
    # Save IP address, to guess the factory when adding the next browser
    factory = form.cleaned_data['factory']
    factory.ip = ip
    factory.save()
    # Redirect to factory detail page
    return HttpResponseRedirect(
        form.cleaned_data['factory'].get_absolute_url())


class InvalidRequest(Exception):
    pass


class PermissionDenied(InvalidRequest):
    pass


def error_page(error):
    """
    Render a simple error message.
    """
    error_title = "invalid request"
    if isinstance(error, PermissionDenied):
        error_title = "permission denied"
    error_message = error.args[0]
    return render_to_response('error.html', locals())


def get_browser(http_request):
    """
    Get browser from POST or GET, and check admin permissions.
    """
    try:
        if 'browser' in http_request.POST:
            browser_id = int(http_request.POST.get('browser', ''))
        else:
            browser_id = int(http_request.GET.get('browser', ''))
    except (KeyError, ValueError):
        raise InvalidRequest(
            "You must specify a numeric browser ID.")
    # Get browser from database
    try:
        browser = Browser.objects.get(id=browser_id)
    except Browser.DoesNotExist:
        raise InvalidRequest(
            "Browser with id=%d does not exist." % browser_id)
    # Permission check
    if browser.factory.admin_id != http_request.user.id:
        raise PermissionDenied(
            "You don't have permission to edit this browser.")
        return render_to_response('error.html', locals())
    return browser


def activation_form(http_request, browser, action='activate'):
    # Show verification form to send a post request
    if action == 'activate':
        form_title = _("activate a browser")
    elif action == 'deactivate':
        form_title = _("deactivate a browser")
    really = _("Do you really want to %(action)s %(browser)s on %(factory)s?")
    really %= {
        'browser': browser,
        'factory': browser.factory,
        'action': action,
        }
    form = u"""
<tr><th></th><td>%s
<input type="hidden" name="browser" value="%d" /></td></tr>
""".strip() % (really, browser.id)
    form_submit = _("Yes, I'm sure")
    form_action = http_request.path
    return render_to_response('form.html', locals())


@login_required
def deactivate(http_request):
    try:
        browser = get_browser(http_request)
        if not browser.active:
            raise InvalidRequest("This browser is already inactive.")
    except InvalidRequest, error:
        return error_page(error)
    # Deactivate browser if this is a proper post request
    if http_request.POST:
        browser.active = False
        browser.save()
        return HttpResponseRedirect(browser.factory.get_absolute_url())
    return activation_form(http_request, browser, 'deactivate')


@login_required
def activate(http_request):
    try:
        browser = get_browser(http_request)
        if browser.active:
            raise InvalidRequest("This browser is already active.")
    except InvalidRequest, error:
        return error_page(error)
    # Deactivate browser if this is a proper post request
    if http_request.POST:
        browser.active = True
        browser.save()
        return HttpResponseRedirect(browser.factory.get_absolute_url())
    return activation_form(http_request, browser)
