from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=200)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Website(models.Model):
    url = models.CharField(max_length=400)
    domain = models.ForeignKey(Domain)
    submitted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.url
