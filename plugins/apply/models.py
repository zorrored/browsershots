from django.db import models
from django.contrib.auth.models import User

PHOTO_UPLOAD_PATH = '/var/www/v04.browsershots.org/static/applicants'


class Applicant(models.Model):
    user = models.ForeignKey(User, editable=False)

    degree = models.CharField(max_length=100, blank=True)
    current_job = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    cambridge = models.CharField(max_length=100, blank=True,
        help_text="Are you willing to move to Cambridge, MA" +
                  " for the summer of 2008?")
    bay_area = models.CharField(max_length=100, blank=True,
        help_text="Are you willing to move to Mountain View, CA" +
                  " for the beginning of 2009?")

    age = models.IntegerField(blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True)
    family = models.CharField(max_length=100, blank=True,
        help_text="Do you have a husband/wife and/or kids?")

    editor = models.CharField(max_length=100, blank=True,
        help_text="Which is your favorite text editor?")
    python = models.CharField(max_length=200, blank=True,
        help_text="Please tell me about your Python experience.")
    django = models.CharField(max_length=200, blank=True)
    sql = models.CharField(max_length=200, blank=True)
    javascript = models.CharField(max_length=200, blank=True)
    web_design = models.CharField(max_length=200, blank=True)
    unix = models.CharField(max_length=200, blank=True)
    networking = models.CharField(max_length=200, blank=True)
    open_source = models.CharField(max_length=200, blank=True,
        help_text="Have you contributed to any open-source projects?")
    music = models.CharField(max_length=200, blank=True,
        help_text="Do you play a musical instrument?" +
                  " Who's your favorite band/artist?")
    urls = models.TextField(max_length=2000, blank=True,
        help_text="Please list URLs for any or all of the" +
        " above questions, one per line.")

    photo = models.ImageField(blank=True, null=True,
                              width_field=True, height_field=True,
                              upload_to=PHOTO_UPLOAD_PATH)
