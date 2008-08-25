from django.db import models
from django.contrib.auth.models import User
from shotserver05.platforms.models import OperatingSystem
from shotserver05.factories.utils import random_secret_key
from shotserver05.utils import granular_update


class Factory(models.Model):
    name = models.SlugField(max_length=20, unique=True)
    user = models.ForeignKey(User)
    secret_key = models.CharField(max_length=512, default=random_secret_key)
    operating_system = models.ForeignKey(OperatingSystem)
    hardware = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
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
        return '/factories/%s/' % self.name


class ScreenSize(models.Model):
    factory = models.ForeignKey(Factory)
    width = models.IntegerField()
    height = models.IntegerField()

    class Meta:
        ordering = ('width', 'height')

    def __unicode__(self):
        return '%dx%d' % (self.width, self.height)


class ColorDepth(models.Model):
    factory = models.ForeignKey(Factory)
    bits_per_pixel = models.IntegerField()

    class Meta:
        ordering = ('bits_per_pixel', )

    def __unicode__(self):
        return str(self.bits_per_pixel)


class FactoryStatistics(models.Model):
    factory = models.ForeignKey(Factory)
    date = models.DateField()
    screenshot_count = models.IntegerField()
    error_count = models.IntegerField()
    problem_count = models.IntegerField()

    class Meta:
        ordering = ('date', 'screenshot_count')
