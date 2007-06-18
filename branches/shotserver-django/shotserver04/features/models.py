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
Javascript, Java, Flash versions.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.utils.translation import gettext_lazy as _


def version_str(self):
    if self.version == 'enabled':
        return str(_("enabled"))
    elif self.version == 'disabled':
        return str(_("disabled"))
    else:
        return self.version


def version_q(self):
    field = 'request_group__' + self._meta.module_name
    result = models.Q(**{field + '__isnull': True})
    result |= models.Q(**{field: self.id})
    # Specific installed versions match requests for 'enabled' too.
    if self.version not in ('disabled', 'enabled'):
        result |= models.Q(**{field: 2}) # 2 means 'enabled'
    return result


class Javascript(models.Model):
    version = models.CharField(
        _('version'), maxlength=30,
        help_text=_("e.g. 1.3 / 1.4 / 1.5"))

    class Admin:
        pass

    class Meta:
        verbose_name = _('Javascript version')
        verbose_name_plural = _('Javascript versions')
        ordering = ('version', )

    __str__ = version_str
    features_q = version_q


class Java(models.Model):
    version = models.CharField(
        _('version'), maxlength=30,
        help_text=_("e.g. 1.4 / 1.5 / 1.6"))

    class Admin:
        pass

    class Meta:
        verbose_name = _('Java version')
        verbose_name_plural = _('Java versions')
        ordering = ('version', )

    __str__ = version_str
    features_q = version_q


class Flash(models.Model):
    version = models.CharField(
        _('version'), maxlength=30,
        help_text=_("e.g. 5 / 6 / 7 / 8 / 9"))

    class Admin:
        pass

    class Meta:
        verbose_name = _('Flash version')
        verbose_name_plural = _('Flash versions')
        ordering = ('version', )

    __str__ = version_str
    features_q = version_q
