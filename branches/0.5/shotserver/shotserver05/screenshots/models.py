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
Models for the screenshots app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django.db.models import PositiveIntegerField as UnsignedIntegerField
from django.contrib.auth.models import User
from shotserver05.jobs.models import Job
from shotserver05.factories.models import Factory


class Attempt(models.Model):
    job = models.ForeignKey(Job)
    hashkey = models.SlugField(max_length=32, unique=True)
    factory = models.ForeignKey(Factory)
    started = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.hashkey


class Screenshot(models.Model):
    attempt = models.ForeignKey(Attempt)
    width = UnsignedIntegerField()
    height = UnsignedIntegerField()
    bytes = UnsignedIntegerField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)


class Error(models.Model):
    attempt = models.ForeignKey(Attempt)
    code = UnsignedIntegerField()
    message = models.CharField(max_length=400)
    occurred = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message


class Problem(models.Model):
    screenshot = models.ForeignKey(Screenshot)
    code = UnsignedIntegerField()
    message = models.CharField(max_length=400)
    reporter = models.ForeignKey(User)
    reported = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
