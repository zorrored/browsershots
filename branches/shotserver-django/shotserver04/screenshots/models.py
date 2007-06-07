from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.requests.models import Request
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import Browser


class Screenshot(models.Model):
    hashkey = models.SlugField(
        _('hashkey'), maxlength=32, unique=True)
    request = models.ForeignKey(Request,
        verbose_name=_('request'), raw_id_admin=True)
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'), raw_id_admin=True)
    browser = models.ForeignKey(Browser,
        verbose_name=_('browser'), raw_id_admin=True)
    width = models.IntegerField(
        _('width'))
    height = models.IntegerField(
        _('height'))
    uploaded = models.DateTimeField(
        _('uploaded'), auto_now_add=True)

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

    def __str__(self):
        return self.hashkey

    def get_absolute_url(self):
        return self.get_size_url('original')

    def get_size_url(self, size):
        return "/png/%s/%s/%s.png" % (size, self.hashkey[:2], self.hashkey)

    def preview_img(self, size=100):
        return '<img src="%s" alt="" width="%s" height="%s" />' % (
            self.get_size_url(size), size, self.height * size / self.width)
