from django.db import models


class NewsItem(models.Model):
    title = models.CharField(maxlength=200)
    url = models.CharField(maxlength=200)
    pubdate = models.DateTimeField()

    class Admin:
        pass

    class Meta:
        ordering = ('-pubdate', 'url')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url
