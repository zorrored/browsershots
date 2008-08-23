from django.db import models


class Domain(models.Model):
    domain = models.CharField(max_length=200)


class Website(models.Model):
    url = models.CharField(max_length=400)
    domain = models.ForeignKey(Domain)
