from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from shotserver04.websites.models import Website
from shotserver04.platforms.models import Platform
from shotserver04.factories.models import Factory
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

    class Meta:
        verbose_name = _('request group')
        verbose_name_plural = _('request groups')

    def __str__(self):
        return str(self.website)


class Request(models.Model):
    request_group = models.ForeignKey(RequestGroup, raw_id_admin=True)
    platform = models.ForeignKey(Platform, blank=True, null=True)
    browser_group = models.ForeignKey(BrowserGroup)
    major = models.IntegerField('major', blank=True, null=True)
    minor = models.IntegerField('minor', blank=True, null=True)

    class Admin:
        fields = (
            (None, {'fields': (
            'request_group',
            'platform',
            ('browser_group', 'major', 'minor'),
            )}),
            )
        list_display = ('browser_group', 'major', 'minor', 'platform')

    class Meta:
        verbose_name = _('request')
        verbose_name_plural = _('requests')

    def __str__(self):
        return '%s %d.%d on %s' % (
            self.browser_group.name, self.major, self.minor,
            self.platform.name)
