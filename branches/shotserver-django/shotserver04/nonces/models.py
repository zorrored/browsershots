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
Nonce models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.factories.models import Factory


class Nonce(models.Model):
    """
    Authentication nonce for password encryption.
    """
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'))
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    ip = models.IPAddressField(
        _('IP address'))
    created = models.DateTimeField(
        _('created'), auto_now_add=True)

    def __unicode__(self):
        return self.hashkey

    class Admin:
        list_display = ('hashkey', 'ip', 'created', 'factory')
        list_filter = ('factory', )
        date_hierarchy = 'created'

    class Meta:
        verbose_name = _('nonce')
        verbose_name_plural = _('nonces')
        ordering = ('created', 'hashkey')
