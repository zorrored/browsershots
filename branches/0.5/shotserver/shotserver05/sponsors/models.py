from django.db import models
from django.contrib.auth.models import User


class Sponsor(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True)
