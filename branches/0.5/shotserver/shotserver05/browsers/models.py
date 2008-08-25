from django.db import models
from shotserver05.factories.models import Factory


class BrowserName(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Engine(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class Browser(models.Model):
    factory = models.ForeignKey(Factory)
    user_agent = models.CharField(max_length=200)
    name = models.ForeignKey(BrowserName)
    version = models.CharField(max_length=20)
    major = models.IntegerField()
    minor = models.IntegerField()
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
        return '%d.%d' % (self.major, self.minor)
