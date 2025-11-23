"""
Admin configuration for the homes app.
"""

from django.contrib import admin
from .models import Home, Appliance, ServiceProvider


class ApplianceInline(admin.TabularInline):
    """
    Inline admin for appliances.
    """
    model = Appliance
    extra = 1
    fields = ['appliance_type', 'manufacturer', 'model_number', 'year_installed']


class ServiceProviderInline(admin.TabularInline):
    """
    Inline admin for service providers.
    """
    model = ServiceProvider
    extra = 1
    fields = ['category', 'company_name', 'phone', 'is_verified']


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    """
    Admin interface for homes.
    """
    list_display = ['name', 'owner', 'year_built', 'construction_type', 'climate_zone', 'created_at']
    list_filter = ['construction_type', 'climate_zone', 'has_basement', 'has_attic', 'has_hvac']
    search_fields = ['name', 'owner__username', 'address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'address', 'year_built'),
        }),
        ('Construction', {
            'fields': ('construction_type', 'climate_zone', 'square_footage'),
        }),
        ('Layout', {
            'fields': ('num_bedrooms', 'num_bathrooms'),
        }),
        ('Features', {
            'fields': ('has_basement', 'has_attic', 'has_garage', 'has_hvac', 'has_septic', 'has_well'),
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at'),
        }),
    )
    
    inlines = [ApplianceInline, ServiceProviderInline]


@admin.register(Appliance)
class ApplianceAdmin(admin.ModelAdmin):
    """
    Admin interface for appliances.
    """
    list_display = ['appliance_type', 'home', 'manufacturer', 'year_installed', 'warranty_expiration']
    list_filter = ['appliance_type', 'year_installed']
    search_fields = ['home__name', 'manufacturer', 'model_number']


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    """
    Admin interface for service providers.
    """
    list_display = ['company_name', 'category', 'home', 'phone', 'is_verified']
    list_filter = ['category', 'is_verified']
    search_fields = ['company_name', 'contact_name', 'home__name']
    list_editable = ['is_verified']

