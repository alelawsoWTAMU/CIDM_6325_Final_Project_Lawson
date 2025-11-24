"""
Views for the accounts app.
Handles user registration, authentication, and profile management.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.urls import reverse_lazy
from django.utils import timezone
from .models import User, UserProfile, ExpertProfile
from .forms import CombinedRegistrationForm, UserProfileForm, ExpertProfileForm


class RegisterView(CreateView):
    """
    Combined registration view for homeowners and experts.
    Homeowners get immediate access, experts need admin verification.
    """
    model = User
    form_class = CombinedRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """
        Save the user and handle post-registration logic.
        """
        response = super().form_valid(form)
        account_type = form.cleaned_data.get('account_type')
        
        if account_type == 'homeowner':
            # Log homeowners in automatically
            login(self.request, self.object)
            messages.success(
                self.request,
                f"Welcome to Homestead Compass, {self.object.username}!"
            )
        elif account_type == 'expert':
            # Experts must wait for admin verification
            messages.info(
                self.request,
                f"Thank you for registering, {self.object.username}! "
                "Your expert application has been submitted. "
                "An administrator will review your information and activate your account. "
                "You will receive an email notification when your account is approved."
            )
            return redirect('accounts:login')
        
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Display user profile information.
    """
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        """
        Return the currently logged-in user.
        """
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile information.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """
        Return the currently logged-in user.
        """
        return self.request.user


class ExpertProfileCreateView(LoginRequiredMixin, CreateView):
    """
    Create expert profile application.
    """
    model = ExpertProfile
    form_class = ExpertProfileForm
    template_name = 'accounts/expert_profile_form.html'
    success_url = reverse_lazy('accounts:profile')
    
    def dispatch(self, request, *args, **kwargs):
        """
        Prevent users who already have expert profile from accessing this view.
        """
        if hasattr(request.user, 'expert_profile'):
            messages.info(request, "You already have an expert profile.")
            return redirect('accounts:expert_profile_edit')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Associate expert profile with current user.
        """
        form.instance.user = self.request.user
        messages.success(
            self.request,
            "Your expert application has been submitted! "
            "An administrator will review it and update your status."
        )
        return super().form_valid(form)


class ExpertProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit existing expert profile.
    """
    model = ExpertProfile
    form_class = ExpertProfileForm
    template_name = 'accounts/expert_profile_form.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        """
        Return the expert profile for the current user.
        """
        return get_object_or_404(ExpertProfile, user=self.request.user)
    
    def form_valid(self, form):
        """
        Save changes to expert profile.
        """
        messages.success(self.request, "Your expert profile has been updated.")
        return super().form_valid(form)


class ExpertProfileDetailView(DetailView):
    """
    View expert profile details (public view).
    """
    model = ExpertProfile
    template_name = 'accounts/expert_profile_detail.html'
    context_object_name = 'expert_profile'
    
    def get_object(self):
        """
        Get expert profile by user's username from URL.
        """
        username = self.kwargs.get('username')
        return get_object_or_404(ExpertProfile, user__username=username)

