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
Screenshot models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.requests.models import Request
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class Screenshot(models.Model):
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    request = models.ForeignKey(Request,
        verbose_name=_('request'), raw_id_admin=True)
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'), raw_id_admin=True)
    browser = models.ForeignKey(Browser,
        verbose_name=_('browser'), raw_id_admin=True)
    width = models.IntegerField(
        _('width'))
    height = models.IntegerField(
        _('height'))
    uploaded = models.DateTimeField(
        _('uploaded'), auto_now_add=True)

    class Admin:
        fields = (
            (None, {'fields': (
            ('hashkey', 'request'),
            ('factory', 'browser'),
            ('width', 'height'),
            'message',
            )}),
            )
        list_display = ('hashkey', 'factory', 'browser',
                        'width', 'height', 'uploaded')

    class Meta:
        verbose_name = _('screenshot')
        verbose_name_plural = _('screenshots')

    def __str__(self):
        return self.hashkey

    def get_absolute_url(self):
        return self.get_size_url('original')

    def get_size_url(self, size):
        return "/png/%s/%s/%s.png" % (size, self.hashkey[:2], self.hashkey)

    def preview_img(self, width=160):
        height = self.height * width / self.width
        return ' '.join((
            '<img src="%s" alt=""',
            'style="width:%spx;height:%spx;z-index:0;position:absolute"',
            'onmouseover="larger(this,%s,%s)"',
            'onmouseout="smaller(this,%s,%s)" />',
            )) % (self.get_size_url(width),
            width / 2, height / 2, width, height, width, height)
