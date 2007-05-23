from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators


def hasSlashAfterHostname(field_data, all_data):
    if field_data.count('/') < 3:
        raise validators.ValidationError(
            _("Missing slash after the hostname."))


class Website(models.Model):
    url = models.URLField(
        _('URL'), maxlength=400, unique=True,
        validator_list=[hasSlashAfterHostname])
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)

    class Admin:
        list_display = ('__str__', 'submitted')
        search_fields = ('url', )
        date_hierarchy = 'submitted'

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __str__(self):
        if len(self.url) > 60:
            return self.url[:56] + '...'
        else:
            return self.url

    def get_absolute_url(self):
        if self.url.count('#'):
            return '/websites/%d/' % self.id
        else:
            return '/' + self.url
