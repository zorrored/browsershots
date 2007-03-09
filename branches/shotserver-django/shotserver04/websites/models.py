from django.db import models


class Website(models.Model):
    url = models.URLField('URL', maxlength=400, verify_exists=False)
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.url) > 60:
            return self.url[:56] + '...'
        else:
            return self.url

    class Admin:
        list_display = ('__str__', 'submitted')
        search_fields = ('url', )
        date_hierarchy = 'submitted'
