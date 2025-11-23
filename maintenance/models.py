"""
Models for the maintenance app.
Defines maintenance tasks, schedules, and task completion records.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

User = get_user_model()


class MaintenanceTask(models.Model):
    """
    Represents a type of maintenance task with instructions and guidelines.
    This is a template that can be scheduled for specific homes.
    """
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('biannual', 'Twice per Year'),
        ('annual', 'Annually'),
        ('biennial', 'Every 2 Years'),
        ('as_needed', 'As Needed'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner - Easy DIY'),
        ('intermediate', 'Intermediate - Some Skills Required'),
        ('advanced', 'Advanced - Consider Professional'),
        ('professional', 'Professional Only'),
    ]
    
    CATEGORY_CHOICES = [
        ('hvac', 'HVAC & Climate Control'),
        ('plumbing', 'Plumbing'),
        ('electrical', 'Electrical'),
        ('exterior', 'Exterior & Roof'),
        ('interior', 'Interior'),
        ('appliances', 'Appliances'),
        ('yard', 'Yard & Landscaping'),
        ('safety', 'Safety Systems'),
        ('seasonal', 'Seasonal'),
        ('general', 'General Maintenance'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text='Name of the maintenance task (e.g., "Change HVAC Filter")'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text='URL-friendly version of title'
    )
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    description = models.TextField(
        help_text='Detailed description of what this task involves'
    )
    
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        default='annual'
    )
    
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='beginner'
    )
    
    estimated_time = models.IntegerField(
        help_text='Estimated time in minutes',
        validators=[MinValueValidator(1)],
        null=True,
        blank=True
    )
    
    tools_required = models.TextField(
        blank=True,
        help_text='List of tools needed (one per line or comma-separated)'
    )
    
    step_by_step = models.TextField(
        blank=True,
        help_text='Step-by-step instructions for completing this task'
    )
    
    safety_notes = models.TextField(
        blank=True,
        help_text='Important safety considerations'
    )
    
    video_url = models.URLField(
        blank=True,
        help_text='Link to instructional video (YouTube, etc.)'
    )
    
    # Conditions that affect when this task should be scheduled
    applies_to_old_homes = models.BooleanField(
        default=True,
        help_text='Relevant for homes older than 20 years'
    )
    
    applies_to_new_homes = models.BooleanField(
        default=True,
        help_text='Relevant for newer homes'
    )
    
    requires_basement = models.BooleanField(default=False)
    requires_attic = models.BooleanField(default=False)
    requires_hvac = models.BooleanField(default=False)
    requires_septic = models.BooleanField(default=False)
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this task should appear in recommendations'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'title']
        verbose_name = 'Maintenance Task'
        verbose_name_plural = 'Maintenance Tasks'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('maintenance:task_detail', kwargs={'slug': self.slug})


class Schedule(models.Model):
    """
    A personalized maintenance schedule for a specific home.
    Links tasks to homes with custom scheduling.
    """
    home = models.ForeignKey(
        'homes.Home',
        on_delete=models.CASCADE,
        related_name='maintenance_schedules'
    )
    
    tasks = models.ManyToManyField(
        MaintenanceTask,
        related_name='schedules',
        help_text='Tasks included in this schedule'
    )
    
    scheduled_date = models.DateField(
        help_text='When these tasks should be performed'
    )
    
    is_completed = models.BooleanField(
        default=False,
        help_text='Whether this schedule has been completed'
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When this schedule was marked complete'
    )
    
    notes = models.TextField(
        blank=True,
        help_text='Notes about this maintenance schedule'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['home', 'scheduled_date']),
        ]
    
    def __str__(self):
        return f"Schedule for {self.home.name} on {self.scheduled_date}"
    
    def mark_complete(self):
        """Mark this schedule as completed."""
        from django.utils import timezone
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()


class TaskCompletion(models.Model):
    """
    Historical record of completed maintenance tasks.
    """
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='completions'
    )
    
    completed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='completed_tasks'
    )
    
    completed_date = models.DateTimeField(auto_now_add=True)
    
    actual_time = models.IntegerField(
        null=True,
        blank=True,
        help_text='Actual time spent in minutes'
    )
    
    feedback = models.TextField(
        blank=True,
        help_text='User feedback about the task (difficulty, tips, etc.)'
    )
    
    rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='How helpful were the instructions? (1-5 stars)'
    )
    
    class Meta:
        ordering = ['-completed_date']
    
    def __str__(self):
        task_count = self.schedule.tasks.count()
        return f"Schedule for {self.schedule.home.name} completed on {self.completed_date.date()} ({task_count} tasks)"

