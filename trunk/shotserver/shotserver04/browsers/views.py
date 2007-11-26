# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
Browser views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django import newforms as forms
from django.db import connection
from django.http import HttpResponseRedirect
from django.newforms.util import ErrorList
from django.contrib.auth.models import check_password
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from shotserver04 import settings
from shotserver04.common import error_page
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
    user_agent_lower = user_agent.lower()
    for engine in agents.get_engines():
        if engine.name.lower() in user_agent_lower:
            initial['engine'] = engine.id
            initial['engine_version'] = agents.extract_version(
                user_agent, engine.name)
            break
    # Extract browser group and version from user agent string
    for browser_group in agents.get_browser_groups():
        if browser_group.name.lower() in user_agent_lower:
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
    admin_email = mark_safe(u'<a href="mailto:%s">%s</a>' % (
        settings.ADMINS[0][1], settings.ADMINS[0][0]))
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
        return render_to_response('browsers/add.html', locals(),
            context_instance=RequestContext(http_request))
    # Activate or add browser in the database
    activate_or_add_browser(form.cleaned_data)
    # Save IP address, to guess the factory when adding the next browser
    form.cleaned_data['factory'].update_fields(ip=ip)
    # Redirect to factory detail page
    return HttpResponseRedirect(
        form.cleaned_data['factory'].get_absolute_url())


def activate_or_add_browser(data):
    """
    Add or activate browser in the database.
    """
    activated = activate_browser(data)
    if activated:
        delete_or_deactivate_similar_browsers(data, exclude=activated)
        return
    else:
        delete_or_deactivate_similar_browsers(data)
    # Create new browser with submitted data
    data['active'] = True
    Browser.objects.create(**data)


def activate_browser(data):
    """
    Try to activate existing browser, and update settings.
    """
    existing_browsers = Browser.objects.filter(
        factory=data['factory'],
        user_agent=data['user_agent'],
        browser_group=data['browser_group'],
        version=data['version'],
        javascript=data['javascript'],
        java=data['java'],
        flash=data['flash'],
        )
    if len(existing_browsers) == 0:
        return False
    browser = existing_browsers[0]
    for candidate in existing_browsers:
        if candidate.active:
            browser = candidate
            break
    modified = False
    data['active'] = True
    for field in 'active command major minor engine engine_version'.split():
        if getattr(browser, field) != data[field]:
            setattr(browser, field, data[field])
            modified = True
    if modified:
        browser.save()
    return browser


def delete_or_deactivate_similar_browsers(data, exclude=None):
    """
    Delete or deactivate similar browsers in the database.
    """
    where = u"""(
(factory_id = %s AND user_agent = %s) OR
(factory_id = %s AND browser_group_id = %s AND major = %s AND minor = %s)
)"""
    params = [
        data['factory'].id,
        data['user_agent'],
        data['factory'].id,
        data['browser_group'].id,
        data['major'],
        data['minor'],
        ]
    if exclude:
        where += "AND id != %s"
        params += [exclude.id]
    # Delete old unused versions of the same browsers
    cursor = connection.cursor()
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


class InvalidRequest(Exception):
    """Not a valid post request."""
    title = _("invalid request")


class PermissionDenied(InvalidRequest):
    """User not logged in as factory admin."""
    title = _("permission denied")


def get_browser(http_request):
    """
    Get browser from POST data, and check admin permissions.
    """
    try:
        browser_id = int(http_request.POST.get('browser', ''))
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
    return browser


@login_required
def deactivate(http_request):
    """
    Deactivate the specified browser.
    """
    try:
        browser = get_browser(http_request)
        if not browser.active:
            raise InvalidRequest(_("This browser is already inactive."))
    except InvalidRequest, error:
        return error_page(http_request, error.title, error.args[0])
    browser.active = False
    browser.save()
    return HttpResponseRedirect(browser.factory.get_absolute_url())


@login_required
def activate(http_request):
    """
    Activate the specified browser.
    """
    try:
        browser = get_browser(http_request)
        if browser.active:
            raise InvalidRequest("This browser is already active.")
    except InvalidRequest, error:
        return error_page(http_request, error.title, error.args[0])
    data = dict((field.name, getattr(browser, field.name))
                for field in Browser._meta.fields)
    delete_or_deactivate_similar_browsers(data, exclude=browser)
    browser.active = True
    browser.save()
    return HttpResponseRedirect(browser.factory.get_absolute_url())
