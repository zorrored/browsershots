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
Website models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

import cgi
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators


def has_slash_after_hostname(field_data, all_data):
    """
    Check that the website URL has 3 or more slashes.
    """
    if field_data.count('/') < 3:
        raise validators.ValidationError(
            _("Missing slash after the hostname."))


class Domain(models.Model):
    """
    Normalized domain names.
    """

    name = models.CharField(
        _('name'), maxlength=200, unique=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)

    class Admin:
        list_display = ('__unicode__', 'submitted')
        search_fields = ('name', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domains')

    def __unicode__(self):
        if len(self.name) > 60:
            return self.name[:56] + '...'
        else:
            return self.name


class Website(models.Model):
    """
    URLs of requested web pages, and some background info.
    """

    url = models.URLField(
        _('URL'), maxlength=400, unique=True,
        validator_list=[has_slash_after_hostname])
    domain = models.ForeignKey(Domain,
        verbose_name=_('domain'), raw_id_admin=True)
    content = models.TextField(
        _('content'), blank=True)
    fetched = models.DateTimeField(
        _('fetched'), auto_now_add=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)

    class Admin:
        list_display = ('__unicode__', 'submitted')
        search_fields = ('url', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __unicode__(self):
        if len(self.url) >= 80:
            return cgi.escape(self.url[:76] + '...')
        else:
            return cgi.escape(self.url)

    def get_absolute_url(self):
        """Get absolute URL."""
        if self.url.count('#'):
            return '/websites/%d/' % self.id
        else:
            return '/' + self.url
