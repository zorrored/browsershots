from django.contrib import admin
from shotserver05.jobs.models import Job, Group


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    list_display = ('website', 'user', 'priority', 'submitted')
    raw_id_fields = ('website', )
    ordering = ('-submitted', )
    inlines = (JobInline, )


admin.site.register(Group, GroupAdmin)
admin.site.register(Job)
