from django.db import models
from django.contrib.auth.models import User
from shotserver04.websites.models import Website
from shotserver04.factories.models import OperatingSystemGroup, Factory
from shotserver04.browsers.models import BrowserGroup


class RequestGroup(models.Model):
    website = models.ForeignKey(Website, raw_id_admin=True)
    width = models.IntegerField('screen width', null=True, blank=True)
    bits_per_pixel = models.IntegerField(null=True, blank=True)
    javascript = models.CharField(maxlength=20, blank=True)
    java = models.CharField(maxlength=20, blank=True)
    flash = models.CharField(maxlength=20, blank=True)
    submitter = models.ForeignKey(User, blank=True, null=True)
    submitted = models.DateTimeField(auto_now_add=True)
    expire = models.DateTimeField()

    def __str__(self):
        return str(self.website)

    class Admin:
        fields = (
            (None, {'fields': (
            'website',
            ('width', 'bits_per_pixel'),
            ('javascript', 'java', 'flash'),
            'submitter',
            'expire',
            )}),
            )
        list_display = ('__str__', 'width', 'javascript', 'java', 'flash')
        search_fields = ('website__url', )
        date_hierarchy = 'submitted'


class Request(models.Model):
    request_group = models.ForeignKey(RequestGroup, raw_id_admin=True)
    operating_system_group = models.ForeignKey(OperatingSystemGroup,
        blank=True, null=True)
    browser_group = models.ForeignKey(BrowserGroup)
    major = models.IntegerField('major', blank=True, null=True)
    minor = models.IntegerField('minor', blank=True, null=True)

    def __str__(self):
        return '%s %d.%d' % (self.browser_group.name, self.major, self.minor)

    class Admin:
        fields = (
            (None, {'fields': (
            'request_group',
            'operating_system_group',
            ('browser_group', 'major', 'minor'),
            )}),
            )
        list_display = ('browser_group', 'major', 'minor',
                        'operating_system_group')
