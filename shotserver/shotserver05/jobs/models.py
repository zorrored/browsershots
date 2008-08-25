from django.db import models
from django.contrib.auth.models import User
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import Browser
from shotserver05.websites.models import Website


class Group(models.Model):
    hashkey = models.SlugField(max_length=32)
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User, blank=True, null=True)
    priority = models.IntegerField()
    submitted = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    group = models.ForeignKey(Group)
    platform = models.ForeignKey(Platform)
    browser = models.ForeignKey(Browser)
    major = models.IntegerField()
    minor = models.IntegerField()
