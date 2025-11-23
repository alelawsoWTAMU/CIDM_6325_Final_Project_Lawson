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
            'city',
            'state',
            'zip_code',
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
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., My First House'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '123 Main St'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Austin'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., TX'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 78701'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1995'}),
            'construction_type': forms.Select(attrs={'class': 'form-select'}),
            'climate_zone': forms.Select(attrs={'class': 'form-select'}),
            'square_footage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1500'}),
            'num_bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 3'}),
            'num_bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2', 'step': '0.5'}),
            'has_basement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_attic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_hvac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_septic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_well': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any additional notes...'}),
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
