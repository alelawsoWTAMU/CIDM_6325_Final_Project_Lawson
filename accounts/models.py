"""
Custom user model and authentication-related models for the accounts app.
Extends Django's built-in User model with homeowner-specific fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended user model for homeowners.
    Adds profile information relevant to home maintenance.
    """
    # Profile information
    bio = models.TextField(
        blank=True,
        max_length=500,
        help_text='Brief description about yourself and your home maintenance experience'
    )
    
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text='Your city or region for localized tips'
    )
    
    is_first_time_homeowner = models.BooleanField(
        default=True,
        help_text='Check if this is your first home'
    )
    
    years_of_homeownership = models.IntegerField(
        default=0,
        help_text='How many years have you owned a home?'
    )
    
    # Community engagement
    is_verified_expert = models.BooleanField(
        default=False,
        help_text='Verified as having professional expertise (contractor, etc.)'
    )
    
    expertise_areas = models.CharField(
        max_length=200,
        blank=True,
        help_text='Areas of expertise (e.g., "plumbing, electrical")'
    )
    
    # Preferences
    email_notifications = models.BooleanField(
        default=True,
        help_text='Receive email reminders for scheduled maintenance'
    )
    
    newsletter_subscription = models.BooleanField(
        default=False,
        help_text='Subscribe to home maintenance tips newsletter'
    )
    
    # Timestamps
    profile_updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username
    
    def get_primary_home(self):
        """Get the user's primary (first) home."""
        return self.homes.first()


class UserProfile(models.Model):
    """
    Additional profile information that doesn't belong in the User model.
    Keeps the User model lean while allowing extended profile data.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    phone = models.CharField(max_length=20, blank=True)
    
    # avatar = models.ImageField(
    #     upload_to='avatars/',
    #     blank=True,
    #     null=True,
    #     help_text='Profile picture'
    # )
    # Note: ImageField commented out - requires Pillow package
    # To enable: pip install Pillow, then uncomment this field
    
    timezone = models.CharField(
        max_length=50,
        default='America/Chicago',
        help_text='Your timezone for scheduling reminders'
    )
    
    preferred_units = models.CharField(
        max_length=20,
        choices=[('imperial', 'Imperial (feet, gallons)'), ('metric', 'Metric (meters, liters)')],
        default='imperial'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"

