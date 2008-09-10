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
Models for the jobs app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.db.models import PositiveIntegerField as UnsignedIntegerField
from shotserver05.websites.models import Website
from django.contrib.auth.models import User
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import BrowserName


class JobGroup(models.Model):
    hashkey = models.SlugField(max_length=32, unique=True)
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User, blank=True, null=True)
    priority = UnsignedIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.website.url


class Job(models.Model):
    group = models.ForeignKey(JobGroup)
    platform = models.ForeignKey(Platform)
    browser_name = models.ForeignKey(BrowserName)
    major = UnsignedIntegerField()
    minor = UnsignedIntegerField()

    def __unicode__(self):
        return '%s %s %s.%s' % (self.platform.name,
            self.browser_name.name, self.major, self.minor)
