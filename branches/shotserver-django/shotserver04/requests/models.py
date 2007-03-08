from django.db import models
from django.contrib.auth.models import User
from shotserver04.factories.models import OperatingSystemGroup, Factory
from shotserver04.browsers.models import BrowserGroup, Browser


class Website(models.Model):
    url = models.URLField('URL', maxlength=400, verify_exists=False)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

    class Admin:
        list_display = ('url', 'submitted')


class RequestGroup(models.Model):
    website = models.ForeignKey(Website)
    width = models.IntegerField('screen width')
    bits_per_pixel = models.IntegerField(null=True, blank=True)
    javascript = models.CharField(maxlength=20, null=True, blank=True)
    java = models.CharField(maxlength=20, null=True, blank=True)
    flash = models.CharField(maxlength=20, null=True, blank=True)
    submitted = models.DateTimeField(auto_now_add=True)
    submitter = models.ForeignKey(User, null=True)
    expire = models.DateTimeField()

    def __str__(self):
        return self.website.url

    class Admin:
        list_display = ('website', 'width', 'submitted')


class Request(models.Model):
    request_group = models.ForeignKey(RequestGroup)
    operating_system_group = models.ForeignKey(OperatingSystemGroup,
        blank=True, null=True)
    browser_group = models.ForeignKey(BrowserGroup)
    major = models.IntegerField('major', blank=True, null=True)
    minor = models.IntegerField('minor', blank=True, null=True)

    def __str__(self):
        return '%s %d.%d' % (self.browser_group.name, self.major, self.minor)

    class Admin:
        list_display = ('browser_group', 'major', 'minor',
                        'operating_system_group')


class Screenshot(models.Model):
    hashkey = models.SlugField(maxlength=32)
    request = models.ForeignKey(Request)
    factory = models.ForeignKey(Factory)
    browser = models.ForeignKey(Browser, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    message = models.CharField(maxlength=400)
    locked = models.DateTimeField(auto_now_add=True)
    redirected = models.DateTimeField(null=True, blank=True)
    failed = models.DateTimeField(null=True, blank=True)
    uploaded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hashkey

    class Admin:
        list_display = ('hashkey', 'factory', 'browser',
                        'width', 'height', 'locked')
