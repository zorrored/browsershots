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
from django.contrib.auth.models import User
from shotserver05.jobs.models import Job
from shotserver05.factories.models import Factory
from shotserver05.utils.random_keys import random_hash_key


class Attempt(models.Model):
    """
    A screenshot factory is loading a screenshot request.
    """
    job = models.ForeignKey(Job)
    hash_key = models.SlugField(max_length=32, unique=True,
                                default=random_hash_key)
    factory = models.ForeignKey(Factory)
    started = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.hash_key


class Screenshot(models.Model):
    """
    Successfully uploaded screenshot.
    """
    attempt = models.ForeignKey(Attempt)
    width = models.IntegerField()
    height = models.IntegerField()
    bytes = models.IntegerField()
    uploaded = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)


class Error(models.Model):
    """
    Factory error when trying to process or upload a screenshot.
    """
    attempt = models.ForeignKey(Attempt)
    code = models.IntegerField()
    message = models.CharField(max_length=400)
    occurred = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message


class Problem(models.Model):
    """
    User report about a problem with a screenshot.
    """
    screenshot = models.ForeignKey(Screenshot)
    code = models.IntegerField()
    message = models.CharField(max_length=400)
    reporter = models.ForeignKey(User)
    reported = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.message
