from django.contrib import admin
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=("title","owner","priority","completed","due_date","created_at")
    list_filter=("completed","priority","created_at")
    search_fields=("title","description","owner__username")
