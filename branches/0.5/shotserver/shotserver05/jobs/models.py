from django.db import models
from shotserver05.websites.models import Website
from django.contrib.auth.models import User
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import BrowserName


class Group(models.Model):
    hashkey = models.SlugField(max_length=32)
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User, blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)


class Job(models.Model):
    group = models.ForeignKey(Group)
    platform = models.ForeignKey(Platform)
    browser_name = models.ForeignKey(BrowserName)
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()
