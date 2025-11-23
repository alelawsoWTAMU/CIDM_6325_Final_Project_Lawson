"""
Admin configuration for the tips app.
Includes moderation features for community content.
"""

from django.contrib import admin
from django.utils import timezone
from .models import LocalTip, TipComment, TipReport


@admin.register(LocalTip)
class LocalTipAdmin(admin.ModelAdmin):
    """
    Admin interface for local tips with moderation features.
    """
    list_display = ['title', 'author', 'category', 'location', 'status', 'upvote_count', 'views', 'is_featured', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'location']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
    date_hierarchy = 'created_at'
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'content'),
        }),
        ('Location', {
            'fields': ('location', 'climate_zone'),
        }),
        ('Moderation', {
            'fields': ('status', 'moderated_by', 'moderated_at', 'moderation_notes'),
        }),
        ('Engagement', {
            'fields': ('views', 'is_featured'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    
    actions = ['approve_tips', 'reject_tips', 'flag_tips']
    
    def approve_tips(self, request, queryset):
        """
        Approve selected tips.
        """
        updated = queryset.update(
            status='approved',
            moderated_by=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f"{updated} tips were approved.")
    approve_tips.short_description = "Approve selected tips"
    
    def reject_tips(self, request, queryset):
        """
        Reject selected tips.
        """
        updated = queryset.update(
            status='rejected',
            moderated_by=request.user,
            moderated_at=timezone.now()
        )
        self.message_user(request, f"{updated} tips were rejected.")
    reject_tips.short_description = "Reject selected tips"
    
    def flag_tips(self, request, queryset):
        """
        Flag selected tips for review.
        """
        updated = queryset.update(status='flagged')
        self.message_user(request, f"{updated} tips were flagged for review.")
    flag_tips.short_description = "Flag selected tips for review"


@admin.register(TipComment)
class TipCommentAdmin(admin.ModelAdmin):
    """
    Admin interface for tip comments.
    """
    list_display = ['tip', 'author', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['tip__title', 'author__username', 'content']
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        """
        Show a preview of the comment content.
        """
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(TipReport)
class TipReportAdmin(admin.ModelAdmin):
    """
    Admin interface for tip reports.
    """
    list_display = ['tip', 'reporter', 'reason', 'is_resolved', 'created_at', 'resolved_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['tip__title', 'reporter__username', 'details']
    list_editable = ['is_resolved']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'resolved_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('tip', 'reporter', 'reason', 'details'),
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by', 'resolved_at', 'resolution_notes'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )
    
    actions = ['mark_resolved']
    
    def mark_resolved(self, request, queryset):
        """
        Mark selected reports as resolved.
        """
        updated = queryset.update(
            is_resolved=True,
            resolved_by=request.user,
            resolved_at=timezone.now()
        )
        self.message_user(request, f"{updated} reports were marked as resolved.")
    mark_resolved.short_description = "Mark selected reports as resolved"

