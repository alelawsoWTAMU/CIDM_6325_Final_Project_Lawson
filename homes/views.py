"""
Views for the homes app.
Handles CRUD operations for homes, appliances, and service providers.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Home, Appliance, ServiceProvider
from .forms import HomeForm, ApplianceForm, ServiceProviderForm


class HomeListView(LoginRequiredMixin, ListView):
    """
    List all homes owned by the current user.
    """
    model = Home
    template_name = 'homes/home_list.html'
    context_object_name = 'homes'
    
    def get_queryset(self):
        """
        Return only homes owned by the current user.
        """
        return Home.objects.filter(owner=self.request.user)


class HomeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Display details of a specific home including appliances and service providers.
    """
    model = Home
    template_name = 'homes/home_detail.html'
    context_object_name = 'home'
    
    def test_func(self):
        """
        Ensure the user owns this home.
        """
        home = self.get_object()
        return home.owner == self.request.user
    
    def get_context_data(self, **kwargs):
        """
        Add appliances and service providers to context.
        """
        context = super().get_context_data(**kwargs)
        context['appliances'] = self.object.appliances.all()
        context['service_providers'] = self.object.service_providers.all()
        return context


class HomeCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new home.
    """
    model = Home
    form_class = HomeForm
    template_name = 'homes/home_form.html'
    
    def form_valid(self, form):
        """
        Set the owner to the current user.
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the home detail page after creation.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.pk})


class HomeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an existing home.
    """
    model = Home
    form_class = HomeForm
    template_name = 'homes/home_form.html'
    
    def test_func(self):
        """
        Ensure the user owns this home.
        """
        home = self.get_object()
        return home.owner == self.request.user
    
    def get_success_url(self):
        """
        Redirect to the home detail page after update.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.pk})


class HomeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a home.
    """
    model = Home
    template_name = 'homes/home_confirm_delete.html'
    success_url = reverse_lazy('homes:home_list')
    
    def test_func(self):
        """
        Ensure the user owns this home.
        """
        home = self.get_object()
        return home.owner == self.request.user


# Appliance Views

class ApplianceCreateView(LoginRequiredMixin, CreateView):
    """
    Add an appliance to a home.
    """
    model = Appliance
    form_class = ApplianceForm
    template_name = 'homes/appliance_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Get the home and verify ownership.
        """
        self.home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Associate the appliance with the home.
        """
        form.instance.home = self.home
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.home.pk})


class ApplianceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update an appliance.
    """
    model = Appliance
    form_class = ApplianceForm
    template_name = 'homes/appliance_form.html'
    
    def test_func(self):
        """
        Ensure the user owns the home this appliance belongs to.
        """
        appliance = self.get_object()
        return appliance.home.owner == self.request.user
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.home.pk})


class ApplianceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an appliance.
    """
    model = Appliance
    template_name = 'homes/appliance_confirm_delete.html'
    
    def test_func(self):
        """
        Ensure the user owns the home this appliance belongs to.
        """
        appliance = self.get_object()
        return appliance.home.owner == self.request.user
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.home.pk})


# Service Provider Views

class ServiceProviderCreateView(LoginRequiredMixin, CreateView):
    """
    Add a service provider to a home.
    """
    model = ServiceProvider
    form_class = ServiceProviderForm
    template_name = 'homes/provider_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Get the home and verify ownership.
        """
        self.home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Associate the provider with the home.
        """
        form.instance.home = self.home
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.home.pk})


class ServiceProviderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a service provider.
    """
    model = ServiceProvider
    form_class = ServiceProviderForm
    template_name = 'homes/provider_form.html'
    
    def test_func(self):
        """
        Ensure the user owns the home this provider is associated with.
        """
        provider = self.get_object()
        return provider.home.owner == self.request.user
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.home.pk})


class ServiceProviderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a service provider.
    """
    model = ServiceProvider
    template_name = 'homes/provider_confirm_delete.html'
    
    def test_func(self):
        """
        Ensure the user owns the home this provider is associated with.
        """
        provider = self.get_object()
        return provider.home.owner == self.request.user
    
    def get_success_url(self):
        """
        Redirect to the home detail page.
        """
        return reverse_lazy('homes:home_detail', kwargs={'pk': self.object.home.pk})

