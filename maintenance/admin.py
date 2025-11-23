"""
Admin configuration for the maintenance app.
"""

from django.contrib import admin
from .models import MaintenanceTask, Schedule, TaskCompletion


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    """
    Admin interface for maintenance tasks.
    """
    list_display = ['title', 'category', 'frequency', 'difficulty', 'estimated_time', 'is_active']
    list_filter = ['category', 'frequency', 'difficulty', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'description'),
        }),
        ('Task Details', {
            'fields': ('frequency', 'difficulty', 'estimated_time'),
        }),
        ('Instructions', {
            'fields': ('tools_required', 'step_by_step', 'safety_notes', 'video_url'),
        }),
        ('Applicability', {
            'fields': (
                'applies_to_old_homes', 'applies_to_new_homes',
                'requires_basement', 'requires_attic', 'requires_hvac', 'requires_septic'
            ),
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """
    Admin interface for schedules.
    """
    list_display = ['task', 'home', 'scheduled_date', 'status', 'completed_date', 'recurs']
    list_filter = ['status', 'recurs', 'scheduled_date']
    search_fields = ['task__title', 'home__name', 'home__owner__username']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('home', 'task', 'scheduled_date', 'status'),
        }),
        ('Completion Details', {
            'fields': ('completed_date', 'performed_by', 'cost'),
        }),
        ('Additional Information', {
            'fields': ('notes', 'recurs'),
        }),
    )


@admin.register(TaskCompletion)
class TaskCompletionAdmin(admin.ModelAdmin):
    """
    Admin interface for task completions.
    """
    list_display = ['schedule', 'completed_by', 'completed_date', 'actual_time', 'rating']
    list_filter = ['completed_date', 'rating']
    search_fields = ['schedule__task__title', 'completed_by__username']
    date_hierarchy = 'completed_date'
    readonly_fields = ['completed_date']

