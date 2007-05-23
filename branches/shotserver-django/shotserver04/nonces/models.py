from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.factories.models import Factory


class Nonce(models.Model):
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'))
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    ip = models.IPAddressField(
        _('IP address'))
    created = models.DateTimeField(
        _('created'), auto_now_add=True)

    def __str__(self):
        return self.hashkey

    class Admin:
        list_display = ('hashkey', 'ip', 'created', 'factory')
        list_filter = ('factory', )
        date_hierarchy = 'created'

    class Meta:
        verbose_name = _('nonce')
        verbose_name_plural = _('nonces')
        ordering = ('created', 'hashkey')
