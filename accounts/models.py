"""
Custom user model and authentication-related models for the accounts app.
Extends Django's built-in User model with homeowner-specific fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


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
    
    # Expert status (verified by admin)
    is_verified_expert = models.BooleanField(
        default=False,
        help_text='Verified as having professional expertise (admin-approved)'
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
    
    # Schedule preferences (JSON field for flexible settings)
    schedule_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text='Schedule customization: preferred_frequency, reminder_days_before, auto_reschedule'
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


class ExpertProfile(models.Model):
    """
    Extended profile for verified local experts (contractors, professionals).
    Required fields for users who want to contribute tips as experts.
    """
    TRADE_CHOICES = [
        ('hvac', 'HVAC Technician'),
        ('plumbing', 'Plumber'),
        ('electrical', 'Electrician'),
        ('roofing', 'Roofing Specialist'),
        ('general_contractor', 'General Contractor'),
        ('landscaping', 'Landscaping/Lawn Care'),
        ('pest_control', 'Pest Control'),
        ('home_inspector', 'Home Inspector'),
        ('appliance_repair', 'Appliance Repair'),
        ('handyman', 'Handyman Services'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='expert_profile'
    )
    
    # Company information
    company_name = models.CharField(
        max_length=200,
        help_text='Your business or company name'
    )
    
    trade = models.CharField(
        max_length=50,
        choices=TRADE_CHOICES,
        help_text='Your primary trade or specialty'
    )
    
    # Contact information
    business_phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'
        )],
        help_text='Business phone number'
    )
    
    business_email = models.EmailField(
        help_text='Business email address'
    )
    
    # Business address
    street_address = models.CharField(
        max_length=300,
        help_text='Street address of your business'
    )
    
    city = models.CharField(
        max_length=100,
        help_text='City'
    )
    
    state = models.CharField(
        max_length=50,
        help_text='State or province'
    )
    
    zip_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            regex=r'^\d{5}(-\d{4})?$',
            message='Enter a valid ZIP code (e.g., 12345 or 12345-6789)'
        )],
        help_text='ZIP or postal code'
    )
    
    # Professional credentials
    license_number = models.CharField(
        max_length=100,
        blank=True,
        help_text='Professional license number (if applicable)'
    )
    
    years_in_business = models.PositiveIntegerField(
        default=0,
        help_text='How many years have you been in business?'
    )
    
    insurance_verified = models.BooleanField(
        default=False,
        help_text='Has proof of insurance been verified by admin?'
    )
    
    # Website and social
    website = models.URLField(
        blank=True,
        help_text='Your business website'
    )
    
    # Admin approval
    application_submitted = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_experts'
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Expert Profile'
        verbose_name_plural = 'Expert Profiles'
        ordering = ['-application_submitted']
    
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"
    
    @property
    def full_address(self):
        """Return formatted full address."""
        return f"{self.street_address}, {self.city}, {self.state} {self.zip_code}"

