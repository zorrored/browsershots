from django.db import models
from django.contrib.auth.models import User
from shotserver05.jobs.models import Job
from shotserver05.factories.models import Factory


class Attempt(models.Model):
    job = models.ForeignKey(Job)
    factory = models.ForeignKey(Factory)
    started = models.DateTimeField(auto_now_add=True)


class Screenshot(models.Model):
    attempt = models.ForeignKey(Attempt)
    hashkey = models.CharField(max_length=32, blank=True, null=True)
    width = models.IntegerField()
    height = models.IntegerField()
    bytes = models.IntegerField()
    uploaded = models.DateTimeField(auto_now_add=True)


class Error(models.Model):
    attempt = models.ForeignKey(Attempt)
    code = models.IntegerField()
    message = models.CharField(max_length=400)
    occurred = models.DateTimeField(auto_now_add=True)


class Problem(models.Model):
    screenshot = models.ForeignKey(Screenshot)
    code = models.IntegerField()
    message = models.CharField(max_length=400)
    reporter = models.ForeignKey(User)
    reported = models.DateTimeField(auto_now_add=True)
