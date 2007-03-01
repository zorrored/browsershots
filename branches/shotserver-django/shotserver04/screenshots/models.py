from django.db import models
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class Screenshot(models.Model):
    hashkey = models.CharField(maxlength=32)
    created = models.DateTimeField('date uploaded', auto_now_add=True)
    factory = models.ForeignKey(Factory)
    browser = models.ForeignKey(Browser)
    width = models.IntegerField()
    height = models.IntegerField()
    def __str__(self): return self.hashkey
    class Admin: pass
