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
Factory models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from xmlrpclib import Fault
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture, OperatingSystem


class Factory(models.Model):
    name = models.SlugField(
        _('name'), unique=True,
        help_text=_('Hostname (lowercase)'))
    admin = models.ForeignKey(User,
        verbose_name=_('administrator'))
    architecture = models.ForeignKey(Architecture,
        verbose_name=_('hardware architecture'),
        help_text=_('CPU type (e.g. i686 or PPC)'))
    operating_system = models.ForeignKey(OperatingSystem,
        verbose_name=_('operating system'))
    last_poll = models.DateTimeField(
        _('last poll'), blank=True, null=True)
    last_upload = models.DateTimeField(
        _('last upload'), blank=True, null=True)
    uploads_per_hour = models.IntegerField(
        _('uploads per hour'), blank=True, null=True)
    uploads_per_day = models.IntegerField(
        _('uploads per day'), blank=True, null=True)
    created = models.DateTimeField(
        _('created'), auto_now_add=True)

    class Admin:
        fields = (
            (None, {'fields': ('name', 'admin')}),
            ('Platform', {'fields': ('architecture', 'operating_system')}),
            )
        search_fields = (
            'name',
            'platform__name',
            'operating_system__name',
            'operating_system__codename',
            'operating_system__version',
            'operating_system__distro',
            'architecture__name',
            )
        list_display = ('name', 'operating_system', 'architecture',
                        'last_poll', 'last_upload', 'uploads_per_day',
                        'created')
        date_hierarchy = 'created'

    class Meta:
        verbose_name = _('factory')
        verbose_name_plural = _('factories')
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/factories/%s/' % self.name

    def features_q(self):
        return (self.platform_q() &
                self.screensizes_q() &
                self.colordepths_q() &
                self.browsers_q())

    def platform_q(self):
        return (models.Q(platform__isnull=True) |
                models.Q(platform__id=self.operating_system.platform.id))

    def operating_system_q(self):
        return (models.Q(operating_system__isnull=True) |
                models.Q(operating_system__id=self.operating_system.id))

    def browsers_q(self):
        q = models.Q()
        browsers = self.browser_set.filter(active=True)
        if not len(browsers):
            raise Fault(0,
                "No browsers registered for factory %s." % self.name)
        for browser in browsers:
            q |= browser.features_q()
        return q

    def screensizes_q(self):
        q = models.Q(request_group__width__isnull=True)
        for screensize in self.screensize_set.all():
            q |= models.Q(request_group__width=screensize.width)
        return q

    def colordepths_q(self):
        q = models.Q(request_group__bits_per_pixel__isnull=True)
        for colordepth in self.colordepth_set.all():
            q |= models.Q(request_group__bits_per_pixel=
                          colordepth.bits_per_pixel)
        return q

    def queue_estimate(self):
        """
        Get the median of queue estimates from the browsers.
        """
        estimates = [browser.queue_estimate
                     for browser in self.browser_set.all()
                     if browser.queue_estimate]
        if not estimates:
            return None
        estimates.sort()
        return estimates[len(estimates) / 2]


class ScreenSize(models.Model):
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'),
        edit_inline=models.TABULAR, num_in_admin=3)
    width = models.IntegerField(
        _('width'), core=True)
    height = models.IntegerField(
        _('height'), core=True)

    def __str__(self):
        return '%dx%d' % (self.width, self.height)

    class Admin:
        list_display = ('width', 'height', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('screen size')
        verbose_name_plural = _('screen sizes')
        ordering = ('width', )
        unique_together = (('factory', 'width', 'height'), )


class ColorDepth(models.Model):
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'),
        edit_inline=models.TABULAR, num_in_admin=3)
    bits_per_pixel = models.IntegerField(
        _('bits per pixel'), core=True)

    def __str__(self):
        return '%d' % self.bits_per_pixel

    class Admin:
        list_display = ('bits_per_pixel', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('color depth')
        verbose_name_plural = _('color depths')
        ordering = ('bits_per_pixel', )
        unique_together = (('factory', 'bits_per_pixel'), )
