"""
Models for the tips app.
Community-driven local knowledge sharing for home maintenance.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

User = get_user_model()


class LocalTip(models.Model):
    """
    User-submitted tips and advice specific to local areas.
    Community members can upvote helpful tips.
    """
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
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tips_authored'
    )
    
    title = models.CharField(
        max_length=200,
        help_text='Brief, descriptive title for the tip'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    content = models.TextField(
        help_text='The actual tip or advice'
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

