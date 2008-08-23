from django.contrib import admin
from shotserver05.browsers.models import Browser, Engine, Version


class BrowserAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class VersionAdmin(admin.ModelAdmin):
    list_display = ('browser', 'version',
                    'engine', 'engine_version',
                    'factory')
    ordering = ('browser', 'version', 'factory')


admin.site.register(Browser, BrowserAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Version, VersionAdmin)
