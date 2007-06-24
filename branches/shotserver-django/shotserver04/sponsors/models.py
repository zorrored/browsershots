from django.db import models


class Sponsor(models.Model):
    """
    Show sponsor links near screenshots from sponsored factories.
    """

    name = models.CharField(
        _('name'), maxlength=50)
    url = models.URLField(
        _('URL'), maxlength=400, unique=True)

    class Admin:
        list_display = ('name', 'url')

    class Meta:
        verbose_name = _('sponsor')
        verbose_name_plural = _('sponsors')
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
