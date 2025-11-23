"""
Admin configuration for the accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User, UserProfile, ExpertProfile


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


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for expert profiles with approval workflow.
    """
    list_display = [
        'company_name',
        'user',
        'trade',
        'city',
        'state',
        'is_approved',
        'application_submitted'
    ]
    list_filter = ['trade', 'state', 'insurance_verified', 'application_submitted']
    search_fields = ['company_name', 'user__username', 'city', 'business_email']
    readonly_fields = ['application_submitted', 'approved_by', 'approved_at']
    
    fieldsets = (
        ('User & Company', {
            'fields': ('user', 'company_name', 'trade')
        }),
        ('Contact Information', {
            'fields': ('business_phone', 'business_email', 'website')
        }),
        ('Business Address', {
            'fields': ('street_address', 'city', 'state', 'zip_code')
        }),
        ('Professional Credentials', {
            'fields': ('license_number', 'years_in_business', 'insurance_verified')
        }),
        ('Approval Status', {
            'fields': ('application_submitted', 'approved_by', 'approved_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_experts', 'revoke_expert_status']
    
    def is_approved(self, obj):
        """Show if expert is approved."""
        return obj.user.is_verified_expert
    is_approved.boolean = True
    is_approved.short_description = 'Approved'
    
    def approve_experts(self, request, queryset):
        """Bulk action to approve expert applications."""
        count = 0
        for expert_profile in queryset:
            if not expert_profile.user.is_verified_expert:
                expert_profile.user.is_verified_expert = True
                expert_profile.user.save()
                expert_profile.approved_by = request.user
                expert_profile.approved_at = timezone.now()
                expert_profile.save()
                count += 1
        
        self.message_user(
            request,
            f"{count} expert profile(s) approved successfully."
        )
    approve_experts.short_description = "Approve selected expert applications"
    
    def revoke_expert_status(self, request, queryset):
        """Bulk action to revoke expert status."""
        count = 0
        for expert_profile in queryset:
            if expert_profile.user.is_verified_expert:
                expert_profile.user.is_verified_expert = False
                expert_profile.user.save()
                count += 1
        
        self.message_user(
            request,
            f"{count} expert status(es) revoked."
        )
    revoke_expert_status.short_description = "Revoke expert status for selected"

