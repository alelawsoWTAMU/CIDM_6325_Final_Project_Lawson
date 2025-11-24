"""
Models for the tips app.
Community-driven local knowledge sharing for home maintenance.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from ckeditor.fields import RichTextField

User = get_user_model()


class LocalTip(models.Model):
    """
    User-submitted tips and advice specific to local areas.
    Community members can upvote helpful tips.
    Supports both expert tips and homeowner questions.
    """
    POST_TYPE_CHOICES = [
        ('tip', 'Expert Tip'),
        ('question', 'Question'),
    ]
    
    CATEGORY_CHOICES = [
        ('hvac', 'HVAC & Climate Control'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('exterior', 'Exterior & Roof'),
        ('interior', 'Interior'),
        ('appliances', 'Appliances'),
        ('yard', 'Yard & Landscaping'),
        ('safety', 'Safety'),
        ('seasonal', 'Seasonal'),
        ('pest_control', 'Pest Control'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged for Review'),
    ]
    
    post_type = models.CharField(
        max_length=20,
        choices=POST_TYPE_CHOICES,
        default='tip',
        help_text='Type of post: expert tip or homeowner question'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tips_authored'
    )
    
    title = models.CharField(
        max_length=200,
        help_text='Brief, descriptive title for the tip or question'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    content = models.TextField(
        help_text='The tip content or question details'
    )
    
    location = models.CharField(
        max_length=200,
        help_text='City, region, or climate zone this tip applies to'
    )
    
    climate_zone = models.CharField(
        max_length=50,
        blank=True,
        help_text='Specific climate zone if applicable'
    )
    
    # Moderation and quality control
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    moderation_notes = models.TextField(
        blank=True,
        help_text='Internal notes from moderators'
    )
    
    moderated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tips_moderated'
    )
    
    moderated_at = models.DateTimeField(null=True, blank=True)
    
    # Community engagement
    upvotes = models.ManyToManyField(
        User,
        related_name='tips_upvoted',
        blank=True
    )
    
    views = models.IntegerField(default=0)
    
    is_featured = models.BooleanField(
        default=False,
        help_text='Highlight this tip as especially useful'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['location', 'category']),
        ]
        verbose_name = 'Local Tip'
        verbose_name_plural = 'Local Tips'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tips:tip_detail', kwargs={'slug': self.slug})
    
    def upvote_count(self):
        """Return the number of upvotes."""
        return self.upvotes.count()
    
    def increment_views(self):
        """Increment the view count."""
        self.views += 1
        self.save(update_fields=['views'])


class TipComment(models.Model):
    """
    Comments on tips for additional discussion and clarification.
    """
    tip = models.ForeignKey(
        LocalTip,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tip_comments'
    )
    
    content = models.TextField()
    
    is_approved = models.BooleanField(
        default=True,
        help_text='Moderators can hide inappropriate comments'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.tip.title}"


class TipReport(models.Model):
    """
    Allows users to report problematic tips for moderator review.
    """
    REASON_CHOICES = [
        ('inaccurate', 'Inaccurate or Misleading Information'),
        ('unsafe', 'Unsafe Advice'),
        ('spam', 'Spam or Advertisement'),
        ('inappropriate', 'Inappropriate Content'),
        ('duplicate', 'Duplicate Tip'),
        ('other', 'Other'),
    ]
    
    tip = models.ForeignKey(
        LocalTip,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tip_reports'
    )
    
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    
    details = models.TextField(
        blank=True,
        help_text='Additional details about the issue'
    )
    
    is_resolved = models.BooleanField(default=False)
    
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_reports'
    )
    
    resolution_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report on '{self.tip.title}' by {self.reporter.username}"


class BlogPost(models.Model):
    """
    Long-form blog articles written by verified experts.
    Includes rich text content and approval workflow.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    CATEGORY_CHOICES = [
        ('hvac', 'HVAC & Climate Control'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('exterior', 'Exterior & Roof'),
        ('interior', 'Interior'),
        ('appliances', 'Appliances'),
        ('yard', 'Yard & Landscaping'),
        ('safety', 'Safety'),
        ('seasonal', 'Seasonal'),
        ('pest_control', 'Pest Control'),
        ('diy', 'DIY Projects'),
        ('general', 'General'),
    ]
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        limit_choices_to={'is_verified_expert': True}
    )
    
    title = models.CharField(
        max_length=200,
        help_text='Compelling title for the blog post'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        help_text='Primary category for this article'
    )
    
    excerpt = models.TextField(
        max_length=500,
        help_text='Brief summary (shown in listings, max 500 characters)'
    )
    
    content = RichTextField(
        help_text='Full article content with rich text formatting'
    )
    
    featured_image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        help_text='Optional featured image for the article'
    )
    
    # SEO and metadata
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text='SEO meta description (max 160 characters)'
    )
    
    tags = models.CharField(
        max_length=200,
        blank=True,
        help_text='Comma-separated tags'
    )
    
    # Publishing and moderation
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    is_featured = models.BooleanField(
        default=False,
        help_text='Featured on blog homepage'
    )
    
    moderation_notes = models.TextField(
        blank=True,
        help_text='Internal notes from moderators'
    )
    
    moderated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts_moderated'
    )
    
    moderated_at = models.DateTimeField(null=True, blank=True)
    
    # Engagement metrics
    view_count = models.PositiveIntegerField(default=0)
    
    upvotes = models.ManyToManyField(
        User,
        related_name='blog_posts_upvoted',
        blank=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('tips:blog_detail', kwargs={'slug': self.slug})
    
    def get_upvote_count(self):
        """Get the number of upvotes for this blog post."""
        return self.upvotes.count()
    
    @property
    def reading_time(self):
        """Estimate reading time in minutes based on word count."""
        word_count = len(self.content.split())
        return max(1, round(word_count / 200))  # Average reading speed
    
    def get_tags_list(self):
        """Return tags as a list."""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]


class BlogComment(models.Model):
    """Comments on blog posts."""
    blog_post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_comments'
    )
    
    content = models.TextField(max_length=2000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on '{self.blog_post.title}'"

