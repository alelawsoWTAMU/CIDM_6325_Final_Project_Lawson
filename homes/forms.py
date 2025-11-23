"""
Forms for the homes app.
Handles home creation/editing, appliances, and service providers.
"""

from django import forms
from .models import Home, Appliance, ServiceProvider


class HomeForm(forms.ModelForm):
    """
    Form for creating and editing homes.
    """
    class Meta:
        model = Home
        fields = [
            'name',
            'address',
            'year_built',
            'construction_type',
            'climate_zone',
            'square_footage',
            'num_bedrooms',
            'num_bathrooms',
            'has_basement',
            'has_attic',
            'has_garage',
            'has_hvac',
            'has_septic',
            'has_well',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ApplianceForm(forms.ModelForm):
    """
    Form for adding and editing appliances.
    """
    class Meta:
        model = Appliance
        fields = [
            'appliance_type',
            'manufacturer',
            'model_number',
            'year_installed',
            'purchase_date',
            'warranty_expiration',
            'notes',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiration': forms.DateInput(attrs={'type': 'date'}),
        }


class ServiceProviderForm(forms.ModelForm):
    """
    Form for adding and editing service providers.
    """
    class Meta:
        model = ServiceProvider
        fields = [
            'category',
            'company_name',
            'contact_name',
            'phone',
            'email',
            'website',
            'address',
            'notes',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
