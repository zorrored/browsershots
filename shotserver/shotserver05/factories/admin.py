from django.contrib import admin
from shotserver05.factories.models import Factory, ScreenSize, ColorDepth


class ScreenSizeInline(admin.TabularInline):
    model = ScreenSize
    extra = 1


class ColorDepthInline(admin.TabularInline):
    model = ColorDepth
    extra = 1


class FactoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    ordering = ('name', )
    inlines = (ScreenSizeInline, ColorDepthInline)


admin.site.register(Factory, FactoryAdmin)
admin.site.register(ScreenSize)
admin.site.register(ColorDepth)
