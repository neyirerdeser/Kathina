from django.contrib import admin
from .models import Event
from .models import Task


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Date information', {'fields': ['start_time','end_time']}),
    ]
admin.site.register(Event,EventAdmin)

class TaskAdmin(admin.ModelAdmin):
    fields = ['name','duration_minutes']
    # fieldsets = [
    #     (None, {'fields': ['name','duration_minutes']}),
    # ]

admin.site.register(Task, TaskAdmin)