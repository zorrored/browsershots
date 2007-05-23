from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.requests.models import Request
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class Screenshot(models.Model):
    hashkey = models.SlugField(maxlength=32, unique=True)
    request = models.ForeignKey(Request, raw_id_admin=True, null=True)
    factory = models.ForeignKey(Factory, raw_id_admin=True)
    browser = models.ForeignKey(Browser, raw_id_admin=True,
                                null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    message = models.CharField('error message', maxlength=400, blank=True)
    locked = models.DateTimeField(auto_now_add=True)
    redirected = models.DateTimeField(null=True, blank=True)
    failed = models.DateTimeField(null=True, blank=True)
    uploaded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.hashkey

    class Admin:
        fields = (
            (None, {'fields': (
            ('hashkey', 'request'),
            ('factory', 'browser'),
            ('width', 'height'),
            'message',
            )}),
            )
        list_display = ('hashkey', 'factory', 'browser',
                        'width', 'height', 'locked')

    class Meta:
        verbose_name = _('screenshot')
        verbose_name_plural = _('screenshots')
