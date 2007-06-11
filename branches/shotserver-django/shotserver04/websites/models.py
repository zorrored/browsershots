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

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators


def hasSlashAfterHostname(field_data, all_data):
    if field_data.count('/') < 3:
        raise validators.ValidationError(
            _("Missing slash after the hostname."))


class Domain(models.Model):
    name = models.CharField(
        _('name'), maxlength=200, unique=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)

    class Admin:
        list_display = ('__str__', 'submitted')
        search_fields = ('name', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('domain')
        verbose_name_plural = _('domains')

    def __str__(self):
        if len(self.name) > 60:
            return self.name[:56] + '...'
        else:
            return self.name


class Website(models.Model):
    url = models.URLField(
        _('URL'), maxlength=400, unique=True,
        validator_list=[hasSlashAfterHostname])
    domain = models.ForeignKey(Domain,
        verbose_name=_('domain'), raw_id_admin=True)
    content = models.TextField(
        _('content'), blank=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)

    class Admin:
        list_display = ('__str__', 'submitted')
        search_fields = ('url', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __str__(self):
        if len(self.url) > 60:
            return self.url[:56] + '...'
        else:
            return self.url

    def get_absolute_url(self):
        if self.url.count('#'):
            return '/websites/%d/' % self.id
        else:
            return '/' + self.url

    def link(self):
        return '<a href="%s">%s</a>' % (
            self.get_absolute_url(), self.url)
