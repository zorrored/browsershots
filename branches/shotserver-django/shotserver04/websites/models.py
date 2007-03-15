from django.db import models
from django.core import validators


def hasSlashAfterHostname(field_data, all_data):
    if field_data.count('/') < 3:
        raise validators.ValidationError(
            "Missing slash after the hostname.")


class Website(models.Model):
    url = models.URLField('URL', maxlength=400, unique=True,
        validator_list=[hasSlashAfterHostname])
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.url) > 60:
            return self.url[:56] + '...'
        else:
            return self.url

    def get_absolute_url(self):
        return '/' + self.url

    class Admin:
        list_display = ('__str__', 'submitted')
        search_fields = ('url', )
        date_hierarchy = 'submitted'
