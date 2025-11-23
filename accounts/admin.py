"""
Admin configuration for the accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin interface for the custom User model.
    """
    list_display = ['username', 'email', 'is_first_time_homeowner', 'location', 'is_verified_expert', 'is_staff']
    list_filter = ['is_first_time_homeowner', 'is_verified_expert', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'location']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Homeowner Information', {
            'fields': ('bio', 'location', 'is_first_time_homeowner', 'years_of_homeownership'),
        }),
        ('Community', {
            'fields': ('is_verified_expert', 'expertise_areas'),
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'newsletter_subscription'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for extended user profiles.
    """
    list_display = ['user', 'phone', 'timezone', 'preferred_units']
    search_fields = ['user__username', 'phone']
    list_filter = ['preferred_units', 'timezone']

