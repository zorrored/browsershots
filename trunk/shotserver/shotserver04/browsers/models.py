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
Browser models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from shotserver04.factories.models import Factory
from shotserver04.features.models import Javascript, Java, Flash


class Engine(models.Model):
    """
    Browser rendering engines like Gecko / KHTML / AppleWebKit.
    """
    name = models.CharField(
        _('name'), max_length=30,
        help_text=_("e.g. Gecko / KHTML / AppleWebKit"))
    maker = models.CharField(
        _('maker'), max_length=30, blank=True)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        verbose_name = _('engine')
        verbose_name_plural = _('engines')
        ordering = ('name', )


class BrowserGroup(models.Model):
    """
    Browser names like Firefox / MSIE / Safari.
    """
    name = models.CharField(
        _('name'), max_length=30,
        help_text=_("e.g. Firefox / MSIE / Safari"))
    maker = models.CharField(
        _('maker'), max_length=30, blank=True)
    terminal = models.BooleanField(
        _('terminal'), help_text=_("Is this a text-mode browser?"))

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        verbose_name = _('browser group')
        verbose_name_plural = _('browser groups')
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class Browser(models.Model):
    """
    Browsers that are installed on a screenshot factory.
    """
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'))
    user_agent = models.CharField(
        _('user agent'), max_length=200)
    browser_group = models.ForeignKey(BrowserGroup,
        verbose_name=_('browser group'))
    version = models.CharField(
        _('version'), max_length=20)
    major = models.IntegerField(
        _('major'))
    minor = models.IntegerField(
        _('minor'))
    engine = models.ForeignKey(Engine,
        verbose_name=_('engine'), blank=True)
    engine_version = models.CharField(
        _('engine version'), max_length=20, blank=True)
    javascript = models.ForeignKey(Javascript,
        verbose_name=_('Javascript'))
    java = models.ForeignKey(Java,
        verbose_name=_('Java'))
    flash = models.ForeignKey(Flash,
        verbose_name=_('Flash'))
    command = models.CharField(
        _('command'), max_length=80, blank=True,
        help_text=_("Leave empty to use default command."))
    active = models.BooleanField(
        _('active'), default=True,
        help_text=_("Designates that this browser is currently installed."))
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
            (None, {'fields': (
            'factory',
            'user_agent',
            'command',
            'browser_group',
            ('version', 'major', 'minor'),
            ('engine', 'engine_version'),
            ('javascript', 'java', 'flash'),
            'active',
            )}),
            )
        list_display = ('browser_group', 'version', 'command',
                        'uploads_per_day', 'factory', 'active')
        list_filter = ('factory', 'browser_group')
        search_fields = ('user_agent', 'command',
                         'javascript', 'java', 'flash')

    class Meta:
        verbose_name = _('browser')
        verbose_name_plural = _('browsers')
        ordering = ('user_agent', )

    def __unicode__(self):
        return u'%s %s' % (self.browser_group.name, self.version)

    def features_q(self):
        """
        SQL to match screenshot requests for this browser.
        """
        group = models.Q(browser_group__id=self.browser_group.id)
        major = models.Q(major__isnull=True) | models.Q(major=self.major)
        minor = models.Q(minor__isnull=True) | models.Q(minor=self.minor)
        javascript = self.javascript.features_q()
        java = self.java.features_q()
        flash = self.flash.features_q()
        return (group & major & minor & javascript & java & flash)

    def activation_form(self):
        if self.active:
            action = '/browsers/deactivate/'
            submit_value = capfirst(_("deactivate"))
        else:
            action = '/browsers/activate/'
            submit_value = capfirst(_("activate"))
        browser_id = self.id
        return u"""
<form action="%(action)s" method="post">
<input type="hidden" name="browser" value="%(browser_id)s" />
<input type="submit" name="submit" value="%(submit_value)s" />
</form>
""" % locals()
