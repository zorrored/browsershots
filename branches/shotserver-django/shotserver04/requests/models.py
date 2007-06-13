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
Request models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from xmlrpclib import Fault
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from shotserver04.websites.models import Website
from shotserver04.platforms.models import Platform
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import BrowserGroup, Browser
from shotserver04.screenshots.models import Screenshot


class RequestGroup(models.Model):
    website = models.ForeignKey(Website,
        verbose_name=_('website'), raw_id_admin=True)
    width = models.IntegerField(
        _('screen width'), null=True, blank=True)
    height = models.IntegerField(
        _('screen height'), null=True, blank=True)
    bits_per_pixel = models.IntegerField(
        _('bits per pixel'), null=True, blank=True)
    javascript = models.CharField(
        _('Javascript'), maxlength=20, blank=True)
    java = models.CharField(
        _('Java'), maxlength=20, blank=True)
    flash = models.CharField(
        _('Flash'), maxlength=20, blank=True)
    submitter = models.ForeignKey(User,
        verbose_name=_('submitter'), blank=True, null=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)
    expire = models.DateTimeField(
        _('expire'))

    class Admin:
        fields = (
            (None, {'fields': (
            'website',
            ('width', 'bits_per_pixel'),
            ('javascript', 'java', 'flash'),
            'submitter',
            'expire',
            )}),
            )
        list_display = ('__str__', 'width', 'javascript', 'java', 'flash')
        search_fields = ('website__url', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('request group')
        verbose_name_plural = _('request groups')
        ordering = ('-submitted', )

    def __str__(self):
        return str(self.submitted)

    def previews(self):
        result = []
        requests = self.request_set.filter(screenshot__isnull=False)
        for request in requests:
            result.append(request.screenshot.preview_div())
        return '\n'.join(result)


class Request(models.Model):
    request_group = models.ForeignKey(RequestGroup,
        verbose_name=_('request group'), raw_id_admin=True)
    platform = models.ForeignKey(Platform,
        verbose_name=_('platform'), blank=True, null=True)
    browser_group = models.ForeignKey(BrowserGroup,
        verbose_name=_('browser group'))
    major = models.IntegerField(
        _('major'), blank=True, null=True)
    minor = models.IntegerField(
        _('minor'), blank=True, null=True)
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'), blank=True, null=True)
    locked = models.DateTimeField(
        _('locked'), blank=True, null=True)
    browser = models.ForeignKey(Browser,
        verbose_name=_('browser'), raw_id_admin=True,
        blank=True, null=True)
    redirected = models.DateTimeField(
        _('redirected'), blank=True, null=True)
    screenshot = models.ForeignKey(Screenshot,
        verbose_name=_('screenshot'), raw_id_admin=True,
        blank=True, null=True)

    class Admin:
        fields = (
            (None, {'fields': (
            'request_group',
            'platform',
            ('browser_group', 'major', 'minor'),
            )}),
            )
        list_display = ('browser_group', 'major', 'minor', 'platform')

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')

    def __str__(self):
        return '%s %d.%d on %s' % (
            self.browser_group.name, self.major, self.minor,
            self.platform.name)

    def check_factory_lock(self, factory):
        if self.factory is None:
            raise Fault(0,
                "Request %d was not locked." % self.id)
        if factory != self.factory:
            raise Fault(0,
                "Request %d was locked by factory %s." %
                (self.id, self.factory.name))
