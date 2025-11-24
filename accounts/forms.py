"""
Forms for the accounts app.
Handles user registration and profile updates.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, ExpertProfile


ACCOUNT_TYPE_CHOICES = [
    ('homeowner', 'Homeowner'),
    ('expert', 'Local Expert (Requires Verification)'),
]


class CombinedRegistrationForm(UserCreationForm):
    """
    Combined registration form for both homeowners and experts.
    Users select account type during registration.
    """
    account_type = forms.ChoiceField(
        choices=ACCOUNT_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='homeowner',
        label='I am registering as a'
    )
    
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    location = forms.CharField(
        max_length=200,
        required=False,
        help_text='Your city or region (optional for homeowners, required for experts)'
    )
    
    # Homeowner fields
    is_first_time_homeowner = forms.BooleanField(
        required=False,
        initial=True,
        label='I am a first-time homeowner'
    )
    
    # Expert fields
    company_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Your business or company name'
    )
    
    trade = forms.ChoiceField(
        choices=[('', '--- Select Trade ---')] + ExpertProfile.TRADE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='Your primary trade or specialty'
    )
    
    business_phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
        help_text='Business phone number'
    )
    
    business_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text='Business email address'
    )
    
    street_address = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St'}),
        help_text='Street address of your business'
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amarillo'}),
        help_text='City'
    )
    
    state = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'TX'}),
        help_text='State or province'
    )
    
    zip_code = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '79101'}),
        help_text='ZIP or postal code'
    )
    
    license_number = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Professional license number (optional)'
    )
    
    years_in_business = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '5'}),
        help_text='How many years have you been in business?'
    )
    
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://yourcompany.com'}),
        help_text='Your business website (optional)'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'account_type')
    
    def clean(self):
        """
        Validate that required fields are provided based on account type.
        """
        cleaned_data = super().clean()
        account_type = cleaned_data.get('account_type')
        
        if account_type == 'expert':
            # Validate expert required fields
            required_expert_fields = {
                'company_name': 'Company name',
                'trade': 'Trade/specialty',
                'business_phone': 'Business phone',
                'business_email': 'Business email',
                'street_address': 'Street address',
                'city': 'City',
                'state': 'State',
                'zip_code': 'ZIP code',
                'years_in_business': 'Years in business',
            }
            
            for field, label in required_expert_fields.items():
                if not cleaned_data.get(field):
                    self.add_error(field, f'{label} is required for expert registration.')
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save user and create ExpertProfile if expert account.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.location = self.cleaned_data.get('location', '')
        
        account_type = self.cleaned_data['account_type']
        
        if account_type == 'homeowner':
            user.is_first_time_homeowner = self.cleaned_data.get('is_first_time_homeowner', True)
            user.is_active = True  # Homeowners are active immediately
        elif account_type == 'expert':
            user.is_first_time_homeowner = False
            user.is_active = True  # Experts can log in but see pending message
            user.is_verified_expert = False  # Will be set to True by admin
        
        if commit:
            user.save()
            
            # Create ExpertProfile if expert registration
            if account_type == 'expert':
                ExpertProfile.objects.create(
                    user=user,
                    company_name=self.cleaned_data['company_name'],
                    trade=self.cleaned_data['trade'],
                    business_phone=self.cleaned_data['business_phone'],
                    business_email=self.cleaned_data['business_email'],
                    street_address=self.cleaned_data['street_address'],
                    city=self.cleaned_data['city'],
                    state=self.cleaned_data['state'],
                    zip_code=self.cleaned_data['zip_code'],
                    license_number=self.cleaned_data.get('license_number', ''),
                    years_in_business=self.cleaned_data.get('years_in_business', 0),
                    website=self.cleaned_data.get('website', ''),
                )
        
        return user


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'bio',
            'location',
            'is_first_time_homeowner',
            'years_of_homeownership',
            'expertise_areas',
            'email_notifications',
            'newsletter_subscription',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class UserProfileExtendedForm(forms.ModelForm):
    """
    Form for extended user profile information (UserProfile model).
    """
    class Meta:
        model = UserProfile
        fields = ['phone', 'timezone', 'preferred_units']
        # Note: 'avatar' field commented out - requires Pillow package


class ExpertProfileForm(forms.ModelForm):
    """
    Form for local expert registration.
    Required for users who want to contribute professional tips.
    """
    class Meta:
        model = ExpertProfile
        fields = [
            'company_name',
            'trade',
            'business_phone',
            'business_email',
            'street_address',
            'city',
            'state',
            'zip_code',
            'license_number',
            'years_in_business',
            'website',
        ]
        widgets = {
            'street_address': forms.TextInput(attrs={'placeholder': '123 Main St'}),
            'city': forms.TextInput(attrs={'placeholder': 'Amarillo'}),
            'state': forms.TextInput(attrs={'placeholder': 'TX'}),
            'zip_code': forms.TextInput(attrs={'placeholder': '79101'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://yourcompany.com'}),
        }
        help_texts = {
            'business_phone': 'Format: +1234567890 or 1234567890',
            'license_number': 'Leave blank if not applicable',
            'website': 'Your business website (optional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields more prominent
        self.fields['company_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['trade'].widget.attrs.update({'class': 'form-select'})
        self.fields['business_email'].widget.attrs.update({'class': 'form-control'})
