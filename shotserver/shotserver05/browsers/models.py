# browsershots.org - Test your web design in different browsers
# Copyright (C) 2008 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Browsershots. If not, see <http://www.gnu.org/licenses/>.

"""
Models for browsers app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.db.models import PositiveIntegerField as UnsignedIntegerField
from shotserver05.factories.models import Factory


class BrowserName(models.Model):
    """
    Supported browser name, e.g. Firefox, Safari, Opera.
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Engine(models.Model):
    """
    Supported browser engine, e.g. Gecko, AppleWebKit, Opera.
    """
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Browser(models.Model):
    """
    Specific browser version installed on a screenshot factory.
    """
    factory = models.ForeignKey(Factory)
    user_agent = models.CharField(max_length=200)
    name = models.ForeignKey(BrowserName)
    version = models.CharField(max_length=20)
    major = UnsignedIntegerField()
    minor = UnsignedIntegerField()
    engine = models.ForeignKey(Engine)
    engine_version = models.CharField(max_length=20)
    flash = models.CharField(max_length=20, blank=True)
    javascript = models.CharField(max_length=20, blank=True)
    java = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ('factory', 'user_agent')

    def __unicode__(self):
        return '%s/%s' % (self.name.name, self.version)

    def get_short_version(self):
        """
        Get short browser version.
        """
        return '%d.%d' % (self.major, self.minor)
