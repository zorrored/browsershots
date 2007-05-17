from django.db import models
from shotserver04.factories.models import Factory


class Nonce(models.Model):
    factory = models.ForeignKey(Factory)
    hashkey = models.SlugField(maxlength=32, unique=True)
    ip = models.IPAddressField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hashkey

    class Admin:
        list_display = ('hashkey', 'ip', 'created', 'factory')
        list_filter = ('factory', )
        date_hierarchy = 'created'

    class Meta:
        ordering = ('hashkey', )
