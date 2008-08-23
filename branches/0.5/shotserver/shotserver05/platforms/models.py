from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class OperatingSystem(models.Model):
    name = models.CharField(max_length=40)
    version = models.CharField(max_length=20, blank=True)
    codename = models.CharField(max_length=40, blank=True)
    slug = models.SlugField(max_length=60, unique=True)
    platform = models.ForeignKey(Platform)

    def __unicode__(self):
        return self.name
