from django.db import models
from shotserver04.factories.models import Factory


class Engine(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30, blank=True, null=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')


class BrowserGroup(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30, blank=True, null=True)
    terminal = models.BooleanField()

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')


class Browser(models.Model):
    factory = models.ForeignKey(Factory)
    user_agent = models.CharField(maxlength=200, core=True)
    browser_group = models.ForeignKey(BrowserGroup)
    version = models.CharField(maxlength=20)
    major = models.IntegerField('major version number')
    minor = models.IntegerField('minor version number')
    engine = models.ForeignKey(Engine, null=True)
    engine_version = models.CharField(maxlength=20, null=True)
    javascript = models.CharField(maxlength=20, null=True)
    java = models.CharField(maxlength=20, null=True)
    flash = models.CharField(maxlength=20, null=True)
    command = models.CharField(maxlength=80, null=True)
    disabled = models.DateTimeField(blank=True, null=True)
    last_upload = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s %d.%d' % (self.browser_group.name, self.major, self.minor)

    class Admin:
        fields = (
            (None, {'fields': ('factory', 'user_agent',
                               ('browser_group', 'version', 'major', 'minor'),
                               ('engine', 'engine_version'),
                               )}),
            )
        list_display = ('factory', 'browser_group', 'version')
        list_display_links = ('browser_group', 'version')
        list_filter = ('factory', )
