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
Models for the factories app.
"""

__revision__ = "$Rev$"
__date__ = "$Date$"
__author__ = "$Author$"

from django.db import models
from django import forms
from django.contrib.auth.models import User
from shotserver05.platforms.models import OperatingSystem
from shotserver05.utils.random_keys import \
    SECRET_KEY_DEFAULT_LENGTH, random_secret_key
from shotserver05.utils import granular_update


class Factory(models.Model):
    """
    Screenshot factory: a remote machine that makes website screenshots.
    """
    name = models.SlugField(max_length=20, unique=True)
    user = models.ForeignKey(User)
    secret_key = models.CharField(max_length=SECRET_KEY_DEFAULT_LENGTH,
                                  default=random_secret_key)
    operating_system = models.ForeignKey(OperatingSystem)
    hardware = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    last_upload = models.DateTimeField(editable=False, null=True)
    last_poll = models.DateTimeField(editable=False, null=True)
    last_error = models.DateTimeField(editable=False, null=True)

    update_fields = granular_update.update_fields

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'factories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """
        Get the URL for the factory details page.
        """
        return '/factories/%s/' % self.name


class ScreenSize(models.Model):
    """
    Supported screen resolution for each factory.
    """
    factory = models.ForeignKey(Factory)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        ordering = ('width', 'height')
        unique_together = ('factory', 'width', 'height')

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)

    @staticmethod
    def validate(width, height):
        if width < 240:
            raise forms.ValidationError(
                "Screen width must not be smaller than 240 pixels.")
        if width > 1680:
            raise forms.ValidationError(
                "Screen width must not be greater than 1680 pixels.")
        return True



class ColorDepth(models.Model):
    """
    Supported display color depths for each factory.
    """
    factory = models.ForeignKey(Factory)
    bits_per_pixel = models.IntegerField()

    class Meta:
        ordering = ('bits_per_pixel', )
        unique_together = ('factory', 'bits_per_pixel')

    def __unicode__(self):
        return str(self.bits_per_pixel)

    @staticmethod
    def validate(bits_per_pixel):
        if bits_per_pixel < 1:
            raise forms.ValidationError(
                "Color depth must not be smaller than 1 bit per pixel.")
        if bits_per_pixel > 32:
            raise forms.ValidationError(
                "Color depth must not be greater than 32 bits per pixel.")
        return True


class FactoryStatistics(models.Model):
    """
    Daily statistics for each factory.
    """
    factory = models.ForeignKey(Factory)
    date = models.DateField()
    screenshot_count = models.IntegerField()
    error_count = models.IntegerField()
    problem_count = models.IntegerField()

    class Meta:
        ordering = ('date', 'screenshot_count')
