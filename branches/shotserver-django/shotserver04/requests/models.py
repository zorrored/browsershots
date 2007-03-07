from django.db import models
from shotserver04.factories.models import OperatingSystemGroup
from shotserver04.browsers.models import BrowserGroup


class Website(models.Model):
    url = models.URLField('URL', verify_exists=False)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    class Admin:
        list_display = ('url', 'created')


class RequestGroup(models.Model):
    website = models.ForeignKey(Website)
    width = models.IntegerField('screen width')
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.website.url

    class Admin:
        list_display = ('website', 'width', 'created')


class Request(models.Model):
    requestgroup = models.ForeignKey(
        RequestGroup, verbose_name='request group')
    operatingsystemgroup = models.ForeignKey(
        OperatingSystemGroup, verbose_name='operating system',
        blank=True, null=True)
    browsergroup = models.ForeignKey(
        BrowserGroup, verbose_name='browser')
    major = models.IntegerField('major', blank=True, null=True)
    minor = models.IntegerField('minor', blank=True, null=True)

    def __str__(self):
        return '%s %d.%d' % (self.browsergroup.name, self.major, self.minor)

    class Admin:
        list_display = ('browsergroup', 'major', 'minor',
                        'operatingsystemgroup')


class Screenshot(models.Model):
    hashkey = models.CharField(maxlength=32)
    request = models.ForeignKey(Request)
    factory = models.ForeignKey(Factory)
    browser = models.ForeignKey(Browser, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    locked = models.DateTimeField(auto_now_add=True)
    redirected = models.DateTimeField(null=True, blank=True)
    uploaded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hashkey

    class Admin:
        list_display = ('hashkey', 'factory', 'browser',
                        'width', 'height', 'locked')
