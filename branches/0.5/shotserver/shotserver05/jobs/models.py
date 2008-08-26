from django.db import models
from shotserver05.websites.models import Website
from django.contrib.auth.models import User
from shotserver05.platforms.models import Platform
from shotserver05.browsers.models import BrowserName


class JobGroup(models.Model):
    hashkey = models.SlugField(max_length=32, unique=True)
    website = models.ForeignKey(Website)
    user = models.ForeignKey(User, blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.website.url


class Job(models.Model):
    group = models.ForeignKey(JobGroup)
    platform = models.ForeignKey(Platform)
    browser_name = models.ForeignKey(BrowserName)
    major = models.PositiveIntegerField()
    minor = models.PositiveIntegerField()

    def __unicode__(self):
        return '%s %s %s.%s' % (self.platform.name,
            self.browser_name.name, self.major, self.minor)
