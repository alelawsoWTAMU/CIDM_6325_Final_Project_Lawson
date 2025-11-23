"""
Views for the accounts app.
Handles user registration, authentication, and profile management.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from .models import User, UserProfile
from .forms import UserRegistrationForm, UserProfileForm


class RegisterView(CreateView):
    """
    User registration view.
    Allows new users to create an account.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """
        Save the user and log them in automatically.
        """
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
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

