"""
Forms for the accounts app.
Handles user registration and profile updates.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with additional fields.
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )
    
    location = forms.CharField(
        max_length=200,
        required=False,
        help_text='Your city or region'
    )
    
    is_first_time_homeowner = forms.BooleanField(
        required=False,
        initial=True,
        label='First-time homeowner?'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'location', 'is_first_time_homeowner')
    
    def save(self, commit=True):
        """
        Save the user with email and location.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.location = self.cleaned_data.get('location', '')
        user.is_first_time_homeowner = self.cleaned_data.get('is_first_time_homeowner', True)
        if commit:
            user.save()
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
