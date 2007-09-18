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
URL input form.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import urlparse
from datetime import datetime
from psycopg import IntegrityError
from django import newforms as forms
from django.utils.text import capfirst
from django.db import transaction
from django.newforms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
from shotserver04 import settings
from shotserver04.websites.utils import \
     split_netloc, http_get, count_profanities, \
     HTTP_TIMEOUT, HTTPError, ConnectError, RequestError
from shotserver04.websites.models import Domain, Website

SUPPORTED_SCHEMES = ['http', 'https']

scheme_match = re.compile(r'[A-Za-z0-9\.+-]+:').match


class UrlForm(forms.Form):
    """
    URL input form.
    """
    url = forms.CharField(
        max_length=Website._meta.get_field('url').max_length,
        label=_("Enter your web address here:"))

    def clean_url(self):
        """
        Clean URL and attempt HTTP GET request.
        """
        self.add_scheme()
        self.split_url()
        self.add_slash()
        self.cleaned_data['content'] = self.http_get()
        self.cleaned_data['profanities'] = count_profanities(
            settings.PROFANITIES_LIST,
            self.cleaned_data['url'] + ' ' + self.cleaned_data['content'])
        self.cleaned_data['domain'] = self.get_or_create_domain()
        self.cleaned_data['website'] = self.get_or_create_website()
        return self.cleaned_data['url']

    def add_scheme(self):
        """
        Add http:// if it's missing.
        """
        url = self.cleaned_data['url']
        if not scheme_match(url):
            self.cleaned_data['url'] = 'http://' + url.lstrip('/')

    def split_url(self):
        """
        Parse URL into components.
        """
        url = self.cleaned_data['url']
        self.url_parts = list(urlparse.urlsplit(url, 'http'))
        # print self.url_parts
        if self.url_parts[0] not in SUPPORTED_SCHEMES:
            raise ValidationError(
                unicode(_("URL scheme %(scheme)s is not supported.") %
                        {'scheme': self.url_parts[0]}))
        if not self.url_parts[1]:
            raise ValidationError(
                unicode(_("Malformed URL (server name not specified).")))
        self.netloc_parts = split_netloc(self.url_parts[1])
        # print self.netloc_parts

    def add_slash(self):
        """
        Add slash after hostname if it's missing.
        """
        if not self.url_parts[2]: # path
            self.url_parts[2] = '/'
            self.cleaned_data['url'] = urlparse.urlunsplit(self.url_parts)

    def http_get(self):
        """
        Load page content from remote HTTP server.
        """
        try:
            return http_get(self.cleaned_data['url'])
        except HTTPError, error:
            if isinstance(error, ConnectError):
                text = _("Could not connect to %(hostname)s.")
            elif isinstance(error, RequestError):
                text = _("Could not send HTTP request to %(hostname)s.")
            else:
                text = _("Could not get page content from %(hostname)s.")
            text %= {'hostname': error.hostname}
            if error.message == 'timed out':
                error.message = (
                    _("Server failed to respond within %d seconds.") %
                    HTTP_TIMEOUT)
            elif error.message:
                error.message = capfirst(error.message).rstrip('.') + '.'
            raise ValidationError(' '.join((text, error.message)).strip())

    def get_or_create_domain(self):
        """
        Get or create domain entry in database.
        """
        domain_name = self.netloc_parts[2] # hostname
        if domain_name.startswith('www.'):
            domain_name = domain_name[4:]
        domain, created = Domain.objects.get_or_create(name=domain_name)
        return domain

    def get_or_create_website(self):
        """
        Get or create website entry in database.
        """
        defaults = {}
        defaults['domain'] = self.cleaned_data['domain']
        # defaults['content'] = self.cleaned_data['content']
        defaults['profanities'] = self.cleaned_data['profanities']
        try:
            website, created = Website.objects.get_or_create(
                url=self.cleaned_data['url'], defaults=defaults)
        except IntegrityError, error:
            if not 'websites_website_url_check' in str(error):
                raise
            transaction.rollback()
            raise ValidationError(
                unicode(_("Malformed URL (database integrity error).")))
        # Update content cache
        if not created:
            # website.content = self.cleaned_data['content']
            website.profanities = self.cleaned_data['profanities']
            website.fetched = datetime.now()
            website.save()
        return website
