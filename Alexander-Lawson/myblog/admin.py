from django.contrib import admin

from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ("title", "author", "date_created", "date_updated")
	search_fields = ("title", "content")
	list_filter = ("author", "date_created")
	ordering = ("-date_created",)
	# Make 'date_created' editable in the admin form
	fieldsets = (
		(None, {
			'fields': ("title", "author", "content", "date_created", "date_updated")
		}),
	)
	# Only date_updated is read-only; date_created (publish date) is editable
	readonly_fields = ("date_updated",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ("author", "post", "date_created", "content_preview")
	search_fields = ("content", "author__username")
	list_filter = ("date_created", "author")
	ordering = ("-date_created",)
	readonly_fields = ("date_created", "date_updated")
	
	def content_preview(self, obj):
		return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
	content_preview.short_description = "Content Preview"
