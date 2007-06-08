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
Platform models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.utils.translation import gettext_lazy as _


class Platform(models.Model):
    name = models.CharField(
        _('name'), maxlength=30,
        help_text="e.g. Linux / Windows / Mac")
    order = models.IntegerField(
        _('order'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = _('platform')
        verbose_name_plural = _('platforms')
        ordering = ('order', 'name')


class OperatingSystem(models.Model):
    platform = models.ForeignKey(Platform,
        verbose_name=_('platform'))
    name = models.CharField(
        _('name'), maxlength=30)
    version = models.CharField(
        _('version'), maxlength=30, blank=True)
    codename = models.CharField(
        _('codename'), maxlength=30, blank=True)
    maker = models.CharField(
        _('maker'), maxlength=30, blank=True)

    def __str__(self):
        return '%s %s (%s)' % (self.name, self.version, self.codename)

    class Admin:
        list_display = ('platform', 'name', 'version', 'codename', 'maker')
        list_filter = ('platform', )

    class Meta:
        verbose_name = _('operating system')
        verbose_name_plural = _('operating systems')
        ordering = ('name', 'version')


class Architecture(models.Model):
    name = models.CharField(
        _('name'), maxlength=30)

    def __str__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        verbose_name = _('architecture')
        verbose_name_plural = _('architectures')
        ordering = ('name', )
