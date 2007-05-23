from django.db import models
from django.utils.translation import gettext_lazy as _
from shotserver04.factories.models import Factory


class Engine(models.Model):
    name = models.CharField(
        _('name'), maxlength=30)
    maker = models.CharField(
        _('maker'), maxlength=30, blank=True)

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        verbose_name = _('engine')
        verbose_name_plural = _('engines')
        ordering = ('name', )


class BrowserGroup(models.Model):
    name = models.CharField(
        _('name'), maxlength=30)
    maker = models.CharField(
        _('maker'), maxlength=30, blank=True)
    terminal = models.BooleanField(
        _('terminal'), help_text=_("Is this a text-mode browser?"))

    def __str__(self):
        return self.name

    class Admin:
        list_display = ('name', 'maker')
        search_fields = ('name', 'maker')

    class Meta:
        verbose_name = _('browser group')
        verbose_name_plural = _('browser groups')
        ordering = ('name', )


class Browser(models.Model):
    factory = models.ForeignKey(Factory,
        verbose_name=_('factory'))
    user_agent = models.CharField(
        _('user agent'), maxlength=200)
    browser_group = models.ForeignKey(BrowserGroup,
        verbose_name=_('browser group'))
    version = models.CharField(
        _('version'), maxlength=20)
    major = models.IntegerField(
        _('major'))
    minor = models.IntegerField(
        _('minor'))
    engine = models.ForeignKey(Engine,
        verbose_name=_('engine'), blank=True)
    engine_version = models.CharField(
        _('engine version'), maxlength=20, blank=True)
    javascript = models.CharField(
        _('Javascript'), maxlength=20, blank=True)
    java = models.CharField(
        _('Java'), maxlength=20, blank=True)
    flash = models.CharField(
        _('Flash'), maxlength=20, blank=True)
    command = models.CharField(
        _('command'), maxlength=80, blank=True)
    disabled = models.BooleanField(
        _('disabled'), help_text=_("Is this browser inactive?"))
    last_upload = models.DateTimeField(
        _('last upload'), blank=True, null=True)

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
        verbose_name = _('browser')
        verbose_name_plural = _('browsers')
        ordering = ('user_agent', )
