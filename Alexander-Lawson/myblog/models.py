from django.db import models


class Post(models.Model):
    """
    Blog post model with title, content, author, and timestamps.
    """
    title = models.CharField(max_length=200, help_text="Enter the blog post title")
    content = models.TextField(help_text="Enter the blog post content")
    author = models.CharField(max_length=100, help_text="Enter the author name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def get_preview(self):
        """Return first 200 characters of content for previews."""
        if len(self.content) > 200:
            return self.content[:200] + '...'
        return self.content
