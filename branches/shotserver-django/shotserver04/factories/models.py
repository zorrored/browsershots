from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth.models import User
from shotserver04.platforms.models import Architecture, OperatingSystem


class Factory(models.Model):
    name = models.SlugField(unique=True,
        help_text=_('Hostname (lowercase)'))
    admin = models.ForeignKey(User,
        verbose_name=_('administrator'))
    architecture = models.ForeignKey(Architecture,
        verbose_name=_('hardware architecture'),
        help_text=_('CPU type (e.g. i686 or PPC)'))
    operating_system = models.ForeignKey(OperatingSystem,
        verbose_name=_('operating system'))
    last_poll = models.DateTimeField(
        _("last poll"), blank=True, null=True)
    last_upload = models.DateTimeField(
        _("last upload"), blank=True, null=True)
    uploads_per_hour = models.IntegerField(
        _("uploads per hour"), blank=True, null=True)
    uploads_per_day = models.IntegerField(
        _("uploads per day"), blank=True, null=True)
    created = models.DateTimeField(
        _("created"), auto_now_add=True)

    class Admin:
        fields = (
            (None, {'fields': ('name', 'admin')}),
            ('Platform', {'fields': ('architecture', 'operating_system')}),
            )
        search_fields = (
            'name',
            'platform__name',
            'operating_system__name',
            'operating_system__codename',
            'operating_system__version',
            'operating_system__distro',
            'architecture__name',
            )
        list_display = ('name', 'operating_system', 'architecture',
                        'last_poll', 'last_upload', 'uploads_per_day',
                        'created')
        date_hierarchy = 'created'

    class Meta:
        verbose_name = _('factory')
        verbose_name_plural = _('factories')
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/factories/%s/' % self.name

    def features_q(self):
        return (self.platform_q() &
                self.browsers_q() &
                self.screensizes_q() &
                self.colordepths_q())

    def platform_q(self):
        return (Q(platform=None) |
                Q(platform__id=self.operating_system.platform.id))

    def operating_system_q(self):
        return (Q(operating_system=None) |
                Q(operating_system__id=self.operating_system.id))

    def browsers_q(self):
        q = Q()
        for browser in self.browser_set.all():
            group = Q(browser_group__id=browser.browser_group.id)
            major = Q(major=None) | Q(major=browser.major)
            minor = Q(minor=None) | Q(minor=browser.minor)
            q |= (group & major & minor)
        return q

    def screensizes_q(self):
        q = Q(request_group__width=None)
        for screensize in self.screensize_set.all():
            q |= Q(request_group__width=screensize.width)
        return q

    def colordepths_q(self):
        q = Q(request_group__bits_per_pixel=None)
        for colordepth in self.colordepth_set.all():
            q |= Q(request_group__bits_per_pixel=colordepth.bits_per_pixel)
        return q


class ScreenSize(models.Model):
    factory = models.ForeignKey(Factory,
        edit_inline=models.TABULAR, num_in_admin=3)
    width = models.IntegerField(core=True)
    height = models.IntegerField(core=True)

    def __str__(self):
        return '%dx%d' % (self.width, self.height)

    class Admin:
        list_display = ('width', 'height', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('screen size')
        verbose_name_plural = _('screen sizes')
        ordering = ('width', )
        unique_together = (('factory', 'width', 'height'), )


class ColorDepth(models.Model):
    factory = models.ForeignKey(Factory,
        edit_inline=models.TABULAR, num_in_admin=3)
    bits_per_pixel = models.IntegerField(core=True)

    def __str__(self):
        return '%d' % self.bits_per_pixel

    class Admin:
        list_display = ('bits_per_pixel', 'factory')
        list_filter = ('factory', )

    class Meta:
        verbose_name = _('color depth')
        verbose_name_plural = _('color depths')
        ordering = ('bits_per_pixel', )
        unique_together = (('factory', 'bits_per_pixel'), )
