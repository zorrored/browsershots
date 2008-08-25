from django.contrib import admin
from shotserver05.browsers.models import BrowserName, Engine, Browser


class BrowserNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class EngineAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name', )}
    ordering = ('slug', )


class BrowserAdmin(admin.ModelAdmin):
    list_display = ('browser', 'version',
                    'engine', 'engine_version',
                    'factory')
    ordering = ('browser', 'version', 'factory')


admin.site.register(BrowserName, BrowserNameAdmin)
admin.site.register(Engine, EngineAdmin)
admin.site.register(Browser, BrowserAdmin)
