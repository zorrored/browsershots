from django.db import models
from shotserver04.requests.models import Request
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


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
        date_hierarchy = 'locked'
