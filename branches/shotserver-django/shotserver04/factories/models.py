from django.db import models
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/factories/%s/' % self.name

    def features_sql(self):
        return ' AND '.join((
            self.operating_system_group_sql(),
            self.operating_system_sql(),
            self.browsers_sql(),
            self.screensizes_sql(),
            self.colordepths_sql(),
            ))

    def operating_system_group_sql(self):
        return (
            '(operating_system_group IS NULL OR' +
            ' operating_system_group = %d)' %
            self.operating_system.operating_system_group.id)

    def operating_system_sql(self):
        return (
            '(operating_system IS NULL OR' +
            ' operating_system = %d)' % self.operating_system.id)

    def browsers_sql(self):
        disjunction = []
        # browsers = Browser.objects.select_related().filter(factory=self)
        for browser in self.browser_set.all():
            disjunction.append('(%s)' % ' AND '.join((
                'browser_group = %d' % browser.browser_group.id,
                '(major IS NULL OR major = %d)' % browser.major,
                '(minor IS NULL OR minor = %d)' % browser.minor,
                )))
        return '(%s)' % ' OR '.join(disjunction)

    def screensizes_sql(self):
        disjunction = ['screensize IS NULL']
        for screensize in self.screensize_set.all():
            disjunction.append('screensize = %d' % screensize.width)
        return '(%s)' % ' OR '.join(disjunction)

    def colordepths_sql(self):
        disjunction = ['colordepth IS NULL']
        for colordepth in self.colordepth_set.all():
            disjunction.append('colordepth = %d' % colordepth.bits_per_pixel)
        return '(%s)' % ' OR '.join(disjunction)

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
        list_display = ('name', 'operating_system', 'architecture', 'created')
        date_hierarchy = 'created'

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'factories'


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
