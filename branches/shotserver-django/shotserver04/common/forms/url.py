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
URL input form.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import re
import urlparse
import socket
import httplib
from datetime import datetime
from psycopg import IntegrityError
from django import newforms as forms
from django.utils.text import capfirst
from django.db import transaction
from django.newforms.util import ValidationError
from shotserver04.common.utils import split_netloc
from shotserver04.websites import extract_domain
from shotserver04.websites.models import Domain, Website
from django.utils.translation import ugettext as _

SUPPORTED_SCHEMES = ['http', 'https']
MAX_RESPONSE_SIZE = 10000 # bytes

scheme_match = re.compile(r'[A-Za-z0-9\.+-]+:').match


class UrlForm(forms.Form):
    """
    URL input form.
    """
    url = forms.CharField(
        max_length=Website._meta.get_field('url').maxlength,
        label=_("Enter your web address here:"))

    def clean_url(self):
        """
        Clean URL and attempt HTTP GET request.
        """
        self.add_scheme()
        self.split_url()
        self.add_slash()
        self.http_connect_and_get()
        self.get_or_create_domain()
        self.get_or_create_website()
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
        print self.url_parts
        if self.url_parts[0] not in SUPPORTED_SCHEMES:
            raise ValidationError(
                _("URL scheme %(scheme)s is not supported.") %
                {'scheme': self.url_parts[0]})
        if not self.url_parts[1]:
            raise ValidationError(
                _("Malformed URL (server name not specified)."))
        self.netloc_parts = split_netloc(self.url_parts[1])
        print self.netloc_parts

    def add_slash(self):
        """
        Add slash after hostname if it's missing.
        """
        if not self.url_parts[2]: # path
            self.url_parts[2] = '/'
            self.cleaned_data['url'] = urlparse.urlunsplit(self.url_parts)

    def http_connect_and_get(self):
        """
        Connect to server and get content.
        """
        socket.setdefaulttimeout(10)
        scheme = self.url_parts[0]
        hostname = self.netloc_parts[2]
        if self.netloc_parts[3] is not None:
            hostname += ':' + self.netloc_parts[3]
        self.cleaned_data['hostname'] = hostname
        try:
            if scheme == 'http':
                connection = httplib.HTTPConnection(hostname)
            elif protocol == 'https':
                connection = httplib.HTTPSConnection(hostname)
        except httplib.HTTPException, error:
            raise ValidationError(
                _("Could not connect to %(hostname)s.") % self.cleaned_data)
        try:
            return self.http_get(connection)
        finally:
            connection.close()

    def http_get(self, connection):
        """
        Try to get content with a HTTP request.
        """
        path = self.url_parts[2]
        if self.url_parts[3]:
            path += '?' + self.url_parts[3]
        # Send HTTP request
        try:
            headers = {"User-Agent": "Browsershots URL Check"}
            connection.request('GET', path, headers=headers)
        except socket.error, error:
            try:
                (error_code, error_string) = error.args
            except ValueError:
                error_string = str(error)
            raise ValidationError(' '.join((
                _("Could not send HTTP request to %(hostname)s.") %
                self.cleaned_data,
                capfirst(error_string).rstrip('.') + '.')))
        # Read response
        try:
            response = connection.getresponse()
        except socket.timeout:
            raise ValidationError(' '.join((
                _("Timeout on server %(hostname)s.") % self.cleaned_data,
                _("Please try again later."))))
        self.cleaned_data['content'] = response.read(MAX_RESPONSE_SIZE)
        # Check status code
        if response.status == 200:
            pass

    def get_or_create_domain(self):
        """
        Get or create domain entry in database.
        """
        domain_name = self.netloc_parts[2] # hostname
        if domain_name.startswith('www.'):
            domain_name = domain_name[4:]
        domain, created = Domain.objects.get_or_create(name=domain_name)
        self.cleaned_data['domain'] = domain

    def get_or_create_website(self):
        """
        Get or create website entry in database.
        """
        try:
            website, created = Website.objects.get_or_create(
                url=self.cleaned_data['url'],
                defaults={
                    'domain': self.cleaned_data['domain'],
                    'content': self.cleaned_data['content'],
                    })
        except IntegrityError, error:
            if not 'websites_website_url_check' in str(error):
                raise
            transaction.rollback()
            raise ValidationError(
                _("Malformed URL (database integrity error)."))
        self.cleaned_data['website'] = website
        # Update content cache
        if not created:
            website.content = self.cleaned_data['content']
            website.fetched = datetime.now()
            website.save()
