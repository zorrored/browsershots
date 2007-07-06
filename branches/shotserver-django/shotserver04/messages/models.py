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
Error log models.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from shotserver04.factories.models import Factory


class FactoryError(models.Model):
    """
    Database log for errors in the screenshot factory interface.
    """
    factory = models.ForeignKey(Factory,
        verbose_name=_("factory"))
    code = models.IntegerField(
        _("error code"))
    message = models.CharField(
        _("error message"), maxlength=600)
    occurred = models.DateTimeField(
        _("occurred"), auto_now_add=True)

    class Admin:
        list_display = ('factory', 'code', 'message', 'occurred')
        list_filter = ('factory', 'code')
        date_hierarchy = 'occurred'

    class Meta:
        verbose_name = _("factory error message")
        verbose_name_plural = _("factory error messages")

    def __unicode__(self):
        return self.message
