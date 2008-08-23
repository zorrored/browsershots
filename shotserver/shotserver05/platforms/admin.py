from django.contrib import admin
from shotserver05.platforms.models import Platform, OperatingSystem


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class OperatingSystemAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'version', 'codename', 'platform')
    prepopulated_fields = {'slug': ('codename', )}
    ordering = ('name', 'version')


admin.site.register(Platform, PlatformAdmin)
admin.site.register(OperatingSystem, OperatingSystemAdmin)
