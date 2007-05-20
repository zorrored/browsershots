from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


class Architecture(models.Model):
    name = models.CharField(maxlength=30)

    def __str__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        ordering = ('name', )


class OperatingSystemGroup(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30, blank=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')

    class Meta:
        ordering = ('name', )


class OperatingSystem(models.Model):
    operating_system_group = models.ForeignKey(OperatingSystemGroup)
    distro = models.CharField('distribution', maxlength=30, blank=True)
    version = models.CharField('version number', maxlength=30, blank=True)
    codename = models.CharField(maxlength=30, blank=True)
    mobile = models.BooleanField(
        help_text='mobile device (e.g. cell phone or PDA)')

    def __str__(self):
        return '%s %s %s (%s)' % (self.operating_system_group.name,
                                  self.distro, self.version, self.codename)

    class Admin:
        list_display = ('operating_system_group', 'distro', 'version',
                        'codename', 'mobile')
        list_filter = ('operating_system_group', )

    class Meta:
        ordering = ('codename', )


class Factory(models.Model):
    name = models.SlugField(unique=True, help_text='Hostname (lowercase)')
    admin = models.ForeignKey(User, verbose_name='administrator')
    architecture = models.ForeignKey(Architecture,
        verbose_name='hardware architecture',
        help_text='CPU type (e.g. i386 or PPC)')
    operating_system = models.ForeignKey(OperatingSystem,
        verbose_name='operating system')
    last_poll = models.DateTimeField(blank=True, null=True)
    last_upload = models.DateTimeField(blank=True, null=True)
    uploads_per_hour = models.IntegerField(blank=True, null=True)
    uploads_per_day = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Admin:
        fields = (
            (None, {'fields': ('name', 'admin')}),
            ('Platform', {'fields': ('architecture', 'operating_system')}),
            )
        search_fields = (
            'name',
            'operating_system__operating_system_group__name',
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
        ordering = ('name', )
        verbose_name_plural = 'factories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/factories/%s/' % self.name

    def features_q(self):
        return (self.operating_system_group_q() &
                # self.operating_system_q() &
                self.browsers_q() &
                self.screensizes_q() &
                self.colordepths_q())

    def operating_system_group_q(self):
        return (Q(operating_system_group=None) |
                Q(operating_system_group__id=
                  self.operating_system.operating_system_group.id))

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
        ordering = ('bits_per_pixel', )
        unique_together = (('factory', 'bits_per_pixel'), )
