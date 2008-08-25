from django.contrib import admin
from shotserver05.websites.models import Domain, Website


class WebsiteInline(admin.TabularInline):
    model = Website
    extra = 1


class DomainAdmin(admin.ModelAdmin):
    list_display = ('domain', 'submitted')
    ordering = ('-submitted', )
    inlines = (WebsiteInline, )


class WebsiteAdmin(admin.ModelAdmin):
    list_display_fields = ('url', 'domain', 'submitted')
    raw_id_fields = ('domain', )


admin.site.register(Domain, DomainAdmin)
admin.site.register(Website, WebsiteAdmin)
