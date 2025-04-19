from django.contrib import admin

from mailing_app.models import Task, TaskReceiver, TaskReport
# Register your models here.

class TaskReceiverInline(admin.TabularInline):
    fk_name = 'task'
    model = TaskReceiver

class TaskReportInline(admin.TabularInline):
    fk_name = 'task'
    model = TaskReport

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date',
                    'created_by', 'completed']
    fields = ['title', 'message', 'date',
                    'created_by', 'updated_by', 'completed']
    list_display_links = ['id', 'title']

    inlines = [TaskReceiverInline, TaskReportInline]

