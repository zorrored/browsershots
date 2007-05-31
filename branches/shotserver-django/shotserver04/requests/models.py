from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from shotserver04.websites.models import Website
from shotserver04.platforms.models import Platform
from shotserver04.factories.models import Factory
from shotserver04.browsers.models import BrowserGroup


class RequestGroup(models.Model):
    website = models.ForeignKey(Website,
        verbose_name=_('website'), raw_id_admin=True)
    width = models.IntegerField(
        _('screen width'), null=True, blank=True)
    bits_per_pixel = models.IntegerField(
        _('bits per pixel'), null=True, blank=True)
    javascript = models.CharField(
        _('Javascript'), maxlength=20, blank=True)
    java = models.CharField(
        _('Java'), maxlength=20, blank=True)
    flash = models.CharField(
        _('Flash'), maxlength=20, blank=True)
    submitter = models.ForeignKey(User,
        verbose_name=_('submitter'), blank=True, null=True)
    submitted = models.DateTimeField(
        _('submitted'), auto_now_add=True)
    expire = models.DateTimeField(
        _('expire'))

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
        ordering = ('-submitted', )

    def __str__(self):
        return str(self.website)


class Request(models.Model):
    request_group = models.ForeignKey(RequestGroup,
        verbose_name=_('request group'), raw_id_admin=True)
    platform = models.ForeignKey(Platform,
        verbose_name=_('platform'), blank=True, null=True)
    browser_group = models.ForeignKey(BrowserGroup,
        verbose_name=_('browser group'))
    major = models.IntegerField(
        _('major'), blank=True, null=True)
    minor = models.IntegerField(
        _('minor'), blank=True, null=True)

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
