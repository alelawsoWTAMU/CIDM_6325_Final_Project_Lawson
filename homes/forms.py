"""
Forms for the homes app.
Handles home creation/editing, appliances, and service providers.
Includes multi-step onboarding wizard forms.
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
            'acreage',
            'location_type',
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
            'acreage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 0.25', 'step': '0.01'}),
            'location_type': forms.Select(attrs={'class': 'form-select'}),
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


# ===== Multi-Step Onboarding Wizard Forms =====

class SurveyStep1Form(forms.ModelForm):
    """
    Step 1: Basic Home Information
    Collects address, age, construction details, and size.
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
            'acreage',
            'location_type',
            'num_bedrooms',
            'num_bathrooms',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Home',
                'autofocus': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '123 Main Street'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'State/Province'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ZIP Code'
            }),
            'year_built': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2005'
            }),
            'construction_type': forms.Select(attrs={'class': 'form-select'}),
            'climate_zone': forms.Select(attrs={'class': 'form-select'}),
            'square_footage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2000'
            }),
            'acreage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 0.25',
                'step': '0.01'
            }),
            'location_type': forms.Select(attrs={'class': 'form-select'}),
            'num_bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3'
            }),
            'num_bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2.5',
                'step': '0.5'
            }),
        }


class SurveyStep2Form(forms.ModelForm):
    """
    Step 2: Home Systems & Infrastructure
    Collects information about energy systems, water systems, and specialized infrastructure.
    """
    class Meta:
        model = Home
        fields = [
            'roof_type',
            'roof_age',
            'hvac_type',
            'hvac_age',
            'siding_material',
            'has_basement',
            'has_attic',
            'has_garage',
            'has_hvac',
            'has_septic',
            'has_well',
            'has_solar_panels',
            'has_generator',
            'has_battery_bank',
            'has_wood_stove',
            'has_sump_pump',
            'water_heater_type',
            'has_composting_toilet',
            'has_rainwater_collection',
            'has_irrigation_system',
        ]
        widgets = {
            'roof_type': forms.Select(attrs={'class': 'form-select'}),
            'roof_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age in years (e.g., 10)'
            }),
            'hvac_type': forms.Select(attrs={'class': 'form-select'}),
            'hvac_age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age in years (e.g., 5)'
            }),
            'siding_material': forms.Select(attrs={'class': 'form-select'}),
            'has_basement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_attic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_hvac': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_septic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_well': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_solar_panels': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_generator': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_battery_bank': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_wood_stove': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_sump_pump': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'water_heater_type': forms.Select(attrs={'class': 'form-select'}),
            'has_composting_toilet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_rainwater_collection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_irrigation_system': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SurveyStep3PropertyForm(forms.ModelForm):
    """
    Step 3: Property Features
    Collects information about outdoor features, structures, and land use.
    """
    class Meta:
        model = Home
        fields = [
            'has_fencing',
            'has_barn_outbuilding',
            'has_greenhouse',
            'has_fruit_trees',
            'has_garden_beds',
            'has_pasture',
            'driveway_type',
        ]
        widgets = {
            'has_fencing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_barn_outbuilding': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_greenhouse': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_fruit_trees': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_garden_beds': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_pasture': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'driveway_type': forms.Select(attrs={'class': 'form-select'}),
        }


class SurveyStep4EquipmentForm(forms.ModelForm):
    """
    Step 4: Equipment & Appliances
    Collects information about property equipment and optional appliance details.
    """
    class Meta:
        model = Home
        fields = [
            'has_tractor',
            'has_riding_mower',
            'has_chainsaw',
            'has_farm_implements',
        ]
        widgets = {
            'has_tractor': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_riding_mower': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_chainsaw': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'has_farm_implements': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SurveyStep3ApplianceForm(forms.ModelForm):
    """
    Step 4 (Supplemental): Appliance Information (can be added multiple times)
    Collects detailed appliance tracking data.
    """
    class Meta:
        model = Appliance
        fields = [
            'appliance_type',
            'manufacturer',
            'model_number',
            'serial_number',
            'energy_rating',
            'year_installed',
            'purchase_date',
            'warranty_expiration',
            'last_service_date',
            'notes',
        ]
        widgets = {
            'appliance_type': forms.Select(attrs={'class': 'form-select'}),
            'manufacturer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., GE, Whirlpool, Carrier'
            }),
            'model_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Model number'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Serial number'
            }),
            'energy_rating': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Energy Star, A+'
            }),
            'year_installed': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 2020'
            }),
            'purchase_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'warranty_expiration': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'last_service_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Maintenance notes, issues, etc.'
            }),
        }

