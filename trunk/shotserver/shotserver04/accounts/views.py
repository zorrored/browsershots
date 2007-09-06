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
Account views.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from datetime import datetime, timedelta
from psycopg import IntegrityError
import socket
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import newforms as forms
from django.newforms.util import ErrorList
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from shotserver04 import settings
from shotserver04.factories.models import Factory
from shotserver04.messages.models import FactoryError
from shotserver04.common.preload import preload_foreign_keys
from shotserver04.common import error_page, success_page
from shotserver04.nonces import crypto
from shotserver04.nonces.models import Nonce


@login_required
def profile(http_request):
    """
    Show a user's private profile page.
    """
    factory_table_header = Factory.table_header()
    factory_list = Factory.objects.select_related().filter(
        admin=http_request.user)
    error_list = FactoryError.objects.filter(
        factory__in=factory_list).order_by('-id')[:10]
    preload_foreign_keys(error_list, factory=factory_list)
    if 'shotserver04.points' in settings.INSTALLED_APPS:
        from shotserver04.points import views as points
        latest = points.latest_balance(http_request.user)
        current_balance = latest.current_balance()
    return render_to_response('accounts/profile.html', locals(),
        context_instance=RequestContext(http_request))


class EmailForm(forms.Form):
    """
    Email input for address verification.
    """
    email = forms.EmailField()


def email(http_request):
    """
    Ask user for email address, then send verification message.
    """
    if http_request.user.is_authenticated():
        return error_page(http_request, _("Already signed in"),
_("You already have a user account, and you're currently signed in."))
    form = EmailForm(http_request.POST or None)
    if not form.is_valid():
        form_title = _("email verification")
        form_action = '/accounts/register/'
        form_submit = _("send email")
        form_javascript = "document.getElementById('id_email').focus()"
        return render_to_response('form.html', locals(),
            context_instance=RequestContext(http_request))
    email = form.cleaned_data['email']
    hashkey = crypto.random_md5()
    ip = http_request.META['REMOTE_ADDR']
    Nonce.objects.create(email=email, hashkey=hashkey, ip=ip)
    domain = Site.objects.get_current().domain
    message = """\
Welcome to Browsershots!

If you have not requested this registration email, you may ignore it.

Click the following link (or copy it into your browser's address bar)
to verify your email address and finish the registration process:

http://%(domain)s/accounts/register/%(hashkey)s/

Cheers,
Browsershots
""" % locals()
    try:
        send_mail("Browsershots account registration", message,
                  'noreply@browsershots.org',
                  ['johann@browsershots.org'],
                  fail_silently=False)
    except socket.error, e:
        return error_page(http_request, _("email error"),
            _("Could not send email."), str(e))
    hide_hashkey(hashkey)
    return success_page(http_request, _("email sent"),
_("A registration email was sent to %(email)s.") % locals(),
_("Check your email inbox and follow the instructions in the message."),
_("If your email provider uses graylisting, it may take a few minutes."))


def hide_hashkey(hashkey):
    """
    Remove hashkey from debug output.
    """
    from django.db import connection
    for index, query in enumerate(connection.queries):
        if hashkey in query['sql']:
            query['sql'] = query['sql'].replace(hashkey, '[hidden]')


class RegistrationForm(forms.Form):
    """
    User registration form.
    """
    username = forms.CharField(max_length=20)
    firstname = forms.CharField(max_length=40)
    lastname = forms.CharField(max_length=40)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)
    repeat = forms.CharField(max_length=40, widget=forms.PasswordInput)

    def clean_repeat(self):
        """
        Check that the password repeat is the same.
        """
        if self.cleaned_data['repeat'] != self.cleaned_data['password']:
            raise forms.ValidationError(unicode(
                _("Repeat password is not the same.")))
        return self.cleaned_data['repeat']

    def create_user(self, email):
        """
        Try to create the user in the database.
        Return None if the username is already taken.
        """
        try:
            return User.objects.create_user(self.cleaned_data['username'],
                email, self.cleaned_data['password'])
        except IntegrityError, e:
            if 'duplicate' in str(e).lower():
                self.errors['username'] = ErrorList([
                    _("This username is already taken.")])
            else:
                self.errors[forms.NON_FIELD_ERRORS] = ErrorList([str(e)])

def register(http_request, hashkey):
    """
    Register a new user, if email verification was successful.
    """
    nonce = get_object_or_404(Nonce, hashkey=hashkey)
    ip = http_request.META['REMOTE_ADDR']
    if nonce.ip != ip:
        return error_page(http_request, _("Wrong IP address"),
_("The verification email was requested from a different IP address."))
    if not nonce.email:
        return error_page(http_request, _("Bad verification code"),
_("The verification code has no email address."))
    if nonce.created < datetime.now() - timedelta(minutes=30):
        return error_page(http_request, _("Verification code expired"),
_("The verification email was requested more than 30 minutes ago."))
    form = RegistrationForm(http_request.POST or None)
    user = None
    if form.is_valid():
        user = form.create_user(nonce.email)
    if user is None:
        form_title = _("create a new account")
        form_action = '/accounts/register/%s/' % hashkey
        form_submit = _("create account")
        form_javascript = "document.getElementById('id_username').focus()"
        return render_to_response('form.html', locals(),
            context_instance=RequestContext(http_request))
    user.firstname = form.cleaned_data['firstname']
    user.lastname = form.cleaned_data['lastname']
    user.save()
    return success_page(http_request, _("Account created"),
        _("A new user account was created."),
        _("Click the link in the top right corner to log in."))
