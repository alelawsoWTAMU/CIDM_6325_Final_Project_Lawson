from django.contrib import admin
from django.utils import timezone
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "date_created", "date_updated", "word_count_display")
	search_fields = ("title", "content", "author__username")
	list_filter = ("author", "date_created", "date_updated")
	ordering = ("-date_created",)
	date_hierarchy = "date_created"
	list_per_page = 25
	
	fieldsets = (
		("Post Information", {
			'fields': ("title", "author", "content")
		}),
		("Timestamps", {
			'fields': ("date_created", "date_updated"),
			'classes': ('collapse',)
		}),
	)
	readonly_fields = ("date_updated", "word_count_display")
	
	actions = ['publish_posts', 'unpublish_posts', 'mark_as_featured']
	
	def word_count_display(self, obj):
		"""Display word count for the post content."""
		return len(obj.content.split())
	word_count_display.short_description = "Word Count"
	
	def publish_posts(self, request, queryset):
		"""Bulk action to set posts as published (date_created to now)."""
		updated = queryset.update(date_created=timezone.now())
		self.message_user(request, f"{updated} post(s) marked as published.")
	publish_posts.short_description = "Publish selected posts"
	
	def unpublish_posts(self, request, queryset):
		"""Bulk action to set posts as future-dated (unpublished)."""
		future_date = timezone.now() + timezone.timedelta(days=365)
		updated = queryset.update(date_created=future_date)
		self.message_user(request, f"{updated} post(s) unpublished.")
	unpublish_posts.short_description = "Unpublish selected posts"
	
	def mark_as_featured(self, request, queryset):
		"""Example bulk action (could add featured field in future)."""
		count = queryset.count()
		self.message_user(request, f"{count} post(s) marked as featured (placeholder action).")
	mark_as_featured.short_description = "Mark as featured"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("author", "post", "date_created", "content_preview", "is_recent")
	search_fields = ("content", "author__username", "post__title")
	list_filter = ("date_created", "author", "post")
	ordering = ("-date_created",)
	readonly_fields = ("date_created", "date_updated")
	date_hierarchy = "date_created"
	list_per_page = 50
	
	actions = ['approve_comments', 'mark_as_spam']
	
	def content_preview(self, obj):
		"""Display truncated comment content."""
		return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
	content_preview.short_description = "Content Preview"
	
	def is_recent(self, obj):
		"""Display boolean indicator if comment is less than 24 hours old."""
		return (timezone.now() - obj.date_created).days == 0
	is_recent.boolean = True
	is_recent.short_description = "Recent"
	
	def approve_comments(self, request, queryset):
		"""Bulk action to approve comments (placeholder - could add approved field)."""
		count = queryset.count()
		self.message_user(request, f"{count} comment(s) approved (placeholder action).")
	approve_comments.short_description = "Approve selected comments"
	
	def mark_as_spam(self, request, queryset):
		"""Bulk action to delete spam comments."""
		count = queryset.count()
		queryset.delete()
		self.message_user(request, f"{count} comment(s) deleted as spam.")
	mark_as_spam.short_description = "Delete as spam"

