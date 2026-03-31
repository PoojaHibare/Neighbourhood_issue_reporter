from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'location_name', 'status', 'priority', 'assigned_department', 'created_at')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('location_name', 'description', 'assigned_department')
