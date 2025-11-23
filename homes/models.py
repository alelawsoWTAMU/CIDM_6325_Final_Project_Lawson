"""
Models for the homes app.
Stores information about user homes including construction details,
appliances, and trusted service providers.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Home(models.Model):
    """
    Represents a homeowner's property with key characteristics
    that influence maintenance schedules.
    """
    CONSTRUCTION_TYPES = [
        ('wood_frame', 'Wood Frame'),
        ('brick', 'Brick'),
        ('concrete', 'Concrete'),
        ('steel_frame', 'Steel Frame'),
        ('mixed', 'Mixed Materials'),
    ]
    
    CLIMATE_ZONES = [
        ('tropical', 'Tropical'),
        ('dry', 'Dry/Arid'),
        ('temperate', 'Temperate'),
        ('continental', 'Continental'),
        ('polar', 'Polar'),
        ('midwest', 'Midwestern U.S.'),
        ('northeast', 'Northeastern U.S.'),
        ('southeast', 'Southeastern U.S.'),
        ('southwest', 'Southwestern U.S.'),
        ('northwest', 'Northwestern U.S.'),
    ]
    
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='homes',
        help_text='The homeowner who manages this property'
    )
    
    name = models.CharField(
        max_length=200,
        help_text='A nickname for this home (e.g., "Main House", "Rental Property")'
    )
    
    address = models.TextField(
        blank=True,
        help_text='Street address of the property'
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text='City where the property is located'
    )
    
    state = models.CharField(
        max_length=50,
        blank=True,
        help_text='State/Province where the property is located'
    )
    
    zip_code = models.CharField(
        max_length=10,
        blank=True,
        help_text='ZIP or postal code'
    )
    
    year_built = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2100)],
        help_text='Year the home was constructed'
    )
    
    construction_type = models.CharField(
        max_length=50,
        choices=CONSTRUCTION_TYPES,
        default='wood_frame'
    )
    
    climate_zone = models.CharField(
        max_length=50,
        choices=CLIMATE_ZONES,
        default='temperate'
    )
    
    square_footage = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(100)],
        help_text='Total square footage of the home'
    )
    
    num_bedrooms = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    
    num_bathrooms = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=2.0,
        validators=[MinValueValidator(0.5)],
        help_text='Number of bathrooms (0.5 = half bath)'
    )
    
    has_basement = models.BooleanField(default=False)
    has_attic = models.BooleanField(default=False)
    has_garage = models.BooleanField(default=False)
    has_hvac = models.BooleanField(default=True, help_text='Central heating/cooling')
    has_septic = models.BooleanField(default=False, help_text='Septic system vs municipal sewer')
    has_well = models.BooleanField(default=False, help_text='Well water vs municipal water')
    
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about the property'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Home'
        verbose_name_plural = 'Homes'
    
    def __str__(self):
        return f"{self.name} ({self.owner.username})"
    
    def get_age(self):
        """Calculate the age of the home in years."""
        from datetime import datetime
        return datetime.now().year - self.year_built


class Appliance(models.Model):
    """
    Represents an appliance in a home that requires maintenance.
    """
    APPLIANCE_TYPES = [
        ('hvac', 'HVAC System'),
        ('water_heater', 'Water Heater'),
        ('furnace', 'Furnace'),
        ('ac_unit', 'Air Conditioning Unit'),
        ('refrigerator', 'Refrigerator'),
        ('washer', 'Washing Machine'),
        ('dryer', 'Dryer'),
        ('dishwasher', 'Dishwasher'),
        ('oven', 'Oven/Stove'),
        ('sump_pump', 'Sump Pump'),
        ('garage_door', 'Garage Door Opener'),
        ('other', 'Other'),
    ]
    
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name='appliances'
    )
    
    appliance_type = models.CharField(max_length=50, choices=APPLIANCE_TYPES)
    manufacturer = models.CharField(max_length=200, blank=True)
    model_number = models.CharField(max_length=200, blank=True)
    
    year_installed = models.IntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2100)],
        null=True,
        blank=True
    )
    
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiration = models.DateField(null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appliance_type', '-year_installed']
    
    def __str__(self):
        return f"{self.get_appliance_type_display()} - {self.home.name}"


class ServiceProvider(models.Model):
    """
    Stores contact information for trusted service providers
    (plumbers, electricians, HVAC techs, etc.).
    """
    SERVICE_CATEGORIES = [
        ('plumber', 'Plumber'),
        ('electrician', 'Electrician'),
        ('hvac', 'HVAC Technician'),
        ('roofer', 'Roofer'),
        ('carpenter', 'Carpenter'),
        ('landscaper', 'Landscaper'),
        ('painter', 'Painter'),
        ('handyman', 'Handyman'),
        ('pest_control', 'Pest Control'),
        ('appliance_repair', 'Appliance Repair'),
        ('general_contractor', 'General Contractor'),
        ('other', 'Other'),
    ]
    
    home = models.ForeignKey(
        Home,
        on_delete=models.CASCADE,
        related_name='service_providers'
    )
    
    category = models.CharField(max_length=50, choices=SERVICE_CATEGORIES)
    company_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    address = models.TextField(blank=True)
    
    notes = models.TextField(
        blank=True,
        help_text='Notes about service quality, pricing, availability, etc.'
    )
    
    is_verified = models.BooleanField(
        default=False,
        help_text='Verified by community moderators'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'company_name']
        verbose_name = 'Service Provider'
        verbose_name_plural = 'Service Providers'
    
    def __str__(self):
        return f"{self.company_name} - {self.get_category_display()}"
