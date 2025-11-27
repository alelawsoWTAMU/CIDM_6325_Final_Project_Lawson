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
    
    ROOF_TYPES = [
        ('asphalt_shingle', 'Asphalt Shingle'),
        ('metal', 'Metal'),
        ('tile', 'Tile (Clay/Concrete)'),
        ('slate', 'Slate'),
        ('wood_shake', 'Wood Shake/Shingle'),
        ('flat', 'Flat/Low-Slope'),
        ('other', 'Other'),
    ]
    
    HVAC_TYPES = [
        ('central_ac', 'Central Air Conditioning'),
        ('heat_pump', 'Heat Pump'),
        ('furnace_ac', 'Furnace + AC'),
        ('boiler', 'Boiler System'),
        ('ductless_mini_split', 'Ductless Mini-Split'),
        ('window_units', 'Window Units'),
        ('none', 'No HVAC'),
    ]
    
    SIDING_MATERIALS = [
        ('vinyl', 'Vinyl'),
        ('wood', 'Wood'),
        ('brick', 'Brick'),
        ('stucco', 'Stucco'),
        ('fiber_cement', 'Fiber Cement'),
        ('metal', 'Metal'),
        ('stone', 'Stone/Stone Veneer'),
        ('mixed', 'Mixed Materials'),
    ]
    
    LOCATION_TYPES = [
        ('rural', 'Rural'),
        ('suburban', 'Suburban'),
        ('urban', 'Urban'),
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
    
    acreage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.25,
        validators=[MinValueValidator(0.01)],
        help_text='Total acreage of the property'
    )
    
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPES,
        default='suburban',
        help_text='Rural, suburban, or urban setting'
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
    
    # Advanced Home Systems
    has_solar_panels = models.BooleanField(default=False, help_text='Solar energy system')
    has_generator = models.BooleanField(default=False, help_text='Backup generator')
    has_battery_bank = models.BooleanField(default=False, help_text='Battery storage system')
    has_wood_stove = models.BooleanField(default=False, help_text='Wood stove or fireplace insert')
    has_sump_pump = models.BooleanField(default=False, help_text='Sump pump in basement/crawlspace')
    has_composting_toilet = models.BooleanField(default=False, help_text='Composting toilet system')
    has_rainwater_collection = models.BooleanField(default=False, help_text='Rainwater harvesting/cistern')
    has_irrigation_system = models.BooleanField(default=False, help_text='Automated irrigation system')
    
    # Water Heater Type
    WATER_HEATER_TYPES = [
        ('', 'Not specified'),
        ('tank', 'Tank Water Heater'),
        ('tankless', 'Tankless Water Heater'),
        ('hybrid', 'Hybrid Heat Pump'),
        ('solar', 'Solar Water Heater'),
    ]
    water_heater_type = models.CharField(
        max_length=20,
        choices=WATER_HEATER_TYPES,
        blank=True,
        default='',
        help_text='Type of water heater'
    )
    
    # Property Features
    has_fencing = models.BooleanField(default=False, help_text='Property has fencing')
    has_barn_outbuilding = models.BooleanField(default=False, help_text='Barn or large outbuilding')
    has_greenhouse = models.BooleanField(default=False, help_text='Greenhouse or cold frame')
    has_fruit_trees = models.BooleanField(default=False, help_text='Fruit trees or orchard')
    has_garden_beds = models.BooleanField(default=False, help_text='Garden beds or vegetable garden')
    has_pasture = models.BooleanField(default=False, help_text='Pasture land for livestock')
    
    DRIVEWAY_TYPES = [
        ('', 'Not specified'),
        ('paved', 'Paved (asphalt/concrete)'),
        ('gravel', 'Gravel'),
        ('dirt', 'Dirt/unpaved'),
    ]
    driveway_type = models.CharField(
        max_length=20,
        choices=DRIVEWAY_TYPES,
        blank=True,
        default='',
        help_text='Type of driveway surface'
    )
    
    # Equipment Ownership
    has_tractor = models.BooleanField(default=False, help_text='Tractor or heavy equipment')
    has_riding_mower = models.BooleanField(default=False, help_text='Riding lawn mower')
    has_chainsaw = models.BooleanField(default=False, help_text='Chainsaw or power tools')
    has_farm_implements = models.BooleanField(default=False, help_text='Plow, disc, or farming implements')
    
    # Enhanced features for detailed maintenance scheduling
    roof_type = models.CharField(
        max_length=50,
        choices=ROOF_TYPES,
        blank=True,
        default='',
        help_text='Type of roofing material'
    )
    
    roof_age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        help_text='Age of the roof in years'
    )
    
    hvac_type = models.CharField(
        max_length=50,
        choices=HVAC_TYPES,
        blank=True,
        default='',
        help_text='Type of HVAC system'
    )
    
    hvac_age = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        help_text='Age of the HVAC system in years'
    )
    
    siding_material = models.CharField(
        max_length=50,
        choices=SIDING_MATERIALS,
        blank=True,
        default='',
        help_text='Primary siding/exterior material'
    )
    
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
    
    serial_number = models.CharField(
        max_length=200,
        blank=True,
        help_text='Serial number for warranty and service records'
    )
    
    energy_rating = models.CharField(
        max_length=10,
        blank=True,
        help_text='Energy Star rating or efficiency class (e.g., A+, Energy Star)'
    )
    
    year_installed = models.IntegerField(
        validators=[MinValueValidator(1950), MaxValueValidator(2100)],
        null=True,
        blank=True
    )
    
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiration = models.DateField(null=True, blank=True)
    
    last_service_date = models.DateField(
        null=True,
        blank=True,
        help_text='Date of last professional service or maintenance'
    )
    
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
