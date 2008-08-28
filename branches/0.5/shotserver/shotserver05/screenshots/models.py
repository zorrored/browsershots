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
