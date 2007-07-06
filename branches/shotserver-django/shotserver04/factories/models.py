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
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.utils.http import urlquote
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture, OperatingSystem
from shotserver04.sponsors.models import Sponsor
from shotserver04.common.templatetags import human

FACTORY_FIELDS_HIDE = ('created', )
FACTORY_FIELDS_SECONDS = ('queue_estimate')
FACTORY_FIELDS_TIMESINCE = ('last_poll', 'last_upload', 'created')


class Factory(models.Model):
    """
    Screenshot factory configuration.
    """
    name = models.SlugField(
        _('name'), unique=True,
        help_text=_('Hostname (lowercase)'))
    admin = models.ForeignKey(User,
        verbose_name=_('administrator'))
    sponsor = models.ForeignKey(Sponsor,
        verbose_name=_('sponsor'), blank=True, null=True)
    architecture = models.ForeignKey(Architecture,
        verbose_name=_('hardware architecture'))
    operating_system = models.ForeignKey(OperatingSystem,
        verbose_name=_('operating system'))
    ip = models.IPAddressField(
        _('IP'), blank=True, null=True,
        help_text=_("The last poll came from this IP address."))
    last_poll = models.DateTimeField(
        _('last poll'), blank=True, null=True)
    last_upload = models.DateTimeField(
        _('last upload'), blank=True, null=True)
    uploads_per_hour = models.IntegerField(
        _('uploads per hour'), blank=True, null=True)
    uploads_per_day = models.IntegerField(
        _('uploads per day'), blank=True, null=True)
    queue_estimate = models.IntegerField(
        _('queue estimate'), blank=True, null=True)
    created = models.DateTimeField(
        _('created'), auto_now_add=True)

    class Admin:
        fields = (
            (None, {'fields': ('name', 'admin', 'sponsor')}),
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
                        'last_poll', 'last_upload',
                        'uploads_per_hour', 'uploads_per_day',
                        'queue_estimate', 'created')
        date_hierarchy = 'created'

    class Meta:
        verbose_name = _('factory')
        verbose_name_plural = _('factories')
        ordering = ('name', )

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Get absolute URL."""
        return '/factories/%s/' % urlquote(self.name)

    def features_q(self):
        """Get SQL query to match screenshot requests."""
        return (self.platform_q() &
                self.screensizes_q() &
                self.colordepths_q() &
                self.browsers_q())

    def platform_q(self):
        """Get SQL query to match requested platforms."""
        return (models.Q(platform__isnull=True) |
                models.Q(platform__id=self.operating_system.platform.id))

    def browsers_q(self):
        """Get SQL query to match requested browsers."""
        q = models.Q()
        browsers = self.browser_set.filter(active=True)
        if not len(browsers):
            raise Fault(404,
                u"No browsers registered for factory %s." % self.name)
        for browser in browsers:
            q |= browser.features_q()
        return q

    def screensizes_q(self):
        """Get SQL query to match requested screen sizes."""
        q = models.Q(request_group__width__isnull=True)
        for screensize in self.screensize_set.all():
            q |= models.Q(request_group__width=screensize.width)
        return q

    def colordepths_q(self):
        """Get SQL query to match requested color depths."""
        q = models.Q(request_group__bits_per_pixel__isnull=True)
        for colordepth in self.colordepth_set.all():
            q |= models.Q(request_group__bits_per_pixel=
                          colordepth.bits_per_pixel)
        return q

    @classmethod
    def table_header(cls):
        """
        HTML table header cells for factory list.
        """
        fields = []
        for field in cls._meta.admin.list_display:
            if field in FACTORY_FIELDS_HIDE:
                continue
            try:
                name = cls._meta.get_field(field).verbose_name
            except models.FieldDoesNotExist:
                name = _(field.replace('_', ' '))
            fields.append(u'<th>%s</th>' % human.human_br(capfirst(name)))
        return ''.join(fields)

    def table_row(self):
        """
        HTML table row cells for this factory.
        """
        fields = []
        for field in self._meta.admin.list_display:
            if field in FACTORY_FIELDS_HIDE:
                continue
            value = getattr(self, field)
            if callable(value):
                value = value()
            if field == 'name':
                value = human.human_link(self)
            if field in FACTORY_FIELDS_TIMESINCE:
                value = human.human_timesince(value)
            if field in FACTORY_FIELDS_SECONDS:
                value = human.human_seconds(value)
            if value is None:
                value = ''
            fields.append(u'<td>%s</td>' % value)
        return ''.join(fields)


class ScreenSize(models.Model):
    """
    Supported screen resolutions for screenshot factories.
    """
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'),
        edit_inline=models.TABULAR, num_in_admin=3)
    width = models.IntegerField(
        _('width'), core=True)
    height = models.IntegerField(
        _('height'), core=True)

    class Admin:
        list_display = ('width', 'height', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('screen size')
        verbose_name_plural = _('screen sizes')
        ordering = ('width', )
        unique_together = (('factory', 'width', 'height'), )

    def __unicode__(self):
        return u'%dx%d' % (self.width, self.height)


class ColorDepth(models.Model):
    """
    Supported color depths (bits per pixel) for screenshot factories.
    """
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'),
        edit_inline=models.TABULAR, num_in_admin=3)
    bits_per_pixel = models.IntegerField(
        _('bits per pixel'), core=True)

    class Admin:
        list_display = ('bits_per_pixel', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('color depth')
        verbose_name_plural = _('color depths')
        ordering = ('bits_per_pixel', )
        unique_together = (('factory', 'bits_per_pixel'), )

    def __unicode__(self):
        return unicode(self.bits_per_pixel)
