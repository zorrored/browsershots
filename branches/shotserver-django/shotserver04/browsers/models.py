from django.db import models
from shotserver04.factories.models import Factory


class Engine(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30, blank=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        ordering = ('name', )


class BrowserGroup(models.Model):
    name = models.CharField(maxlength=30)
    maker = models.CharField(maxlength=30, blank=True)
    terminal = models.BooleanField()

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        ordering = ('name', )


class Browser(models.Model):
    factory = models.ForeignKey(Factory)
    user_agent = models.CharField(maxlength=200)
    browser_group = models.ForeignKey(BrowserGroup)
    version = models.CharField(maxlength=20)
    major = models.IntegerField()
    minor = models.IntegerField()
    engine = models.ForeignKey(Engine, blank=True)
    engine_version = models.CharField(maxlength=20, blank=True)
    javascript = models.CharField(maxlength=20, blank=True)
    java = models.CharField(maxlength=20, blank=True)
    flash = models.CharField(maxlength=20, blank=True)
    command = models.CharField(maxlength=80, blank=True)
    disabled = models.BooleanField()
    last_upload = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s %d.%d' % (self.browser_group.name, self.major, self.minor)

    class Admin:
        fields = (
            (None, {'fields': (
            'factory',
            'user_agent',
            ('browser_group', 'command'),
            ('version', 'major', 'minor'),
            ('engine', 'engine_version'),
            ('javascript', 'java', 'flash'),
            'disabled',
            )}),
            )
        list_display = ('browser_group', 'version', 'command', 'factory')
        list_filter = ('factory', 'browser_group')
        search_fields = ('user_agent', 'command',
                         'javascript', 'java', 'flash')

    class Meta:
        ordering = ('user_agent', )
