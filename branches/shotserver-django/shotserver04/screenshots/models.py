from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.requests.models import Request
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class Screenshot(models.Model):
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    request = models.ForeignKey(Request,
        verbose_name=_('request'), raw_id_admin=True, null=True, blank=True)
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'), raw_id_admin=True)
    browser = models.ForeignKey(Browser,
        verbose_name=_('browser'), raw_id_admin=True, null=True, blank=True)
    width = models.IntegerField(
        _('width'), null=True, blank=True)
    height = models.IntegerField(
        _('height'), null=True, blank=True)
    uploaded = models.DateTimeField(
        _('uploaded'), auto_now_add=True)

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
                        'width', 'height', 'uploaded')

    class Meta:
        verbose_name = _('screenshot')
        verbose_name_plural = _('screenshots')
