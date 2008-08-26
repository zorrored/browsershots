from django.contrib import admin
from shotserver05.jobs.models import JobGroup, Job


class JobInline(admin.TabularInline):
    model = Job
    extra = 1


class JobGroupAdmin(admin.ModelAdmin):
    list_display = ('website', 'user', 'priority', 'submitted')
    raw_id_fields = ('website', )
    ordering = ('-submitted', )
    inlines = (JobInline, )


admin.site.register(JobGroup, JobGroupAdmin)
admin.site.register(Job)
