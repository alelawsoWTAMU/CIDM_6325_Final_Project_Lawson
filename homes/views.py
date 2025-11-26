"""
Views for the homes app.
Handles CRUD operations for homes, appliances, and service providers.
Includes multi-step onboarding wizard.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .models import Home, Appliance, ServiceProvider
from .forms import (
    HomeForm, ApplianceForm, ServiceProviderForm,
    SurveyStep1Form, SurveyStep2Form, SurveyStep3ApplianceForm
)


class HomeListView(LoginRequiredMixin, ListView):
    """
    List all homes owned by the current user.
    """
    model = Home
    template_name = 'homes/home_list.html'
    context_object_name = 'home_list'
    
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


# ===== Multi-Step Onboarding Wizard =====

class HomeOnboardingWizardView(LoginRequiredMixin, View):
    """
    Multi-step wizard for comprehensive home onboarding.
    Step 1: Basic home information
    Step 2: Home features and systems
    Step 3: Appliances (optional, repeatable)
    """
    
    def get(self, request, step=1):
        """
        Display the appropriate step of the wizard.
        """
        step = int(step)
        
        # Get session data for pre-filling forms
        step1_data = request.session.get('survey_step1', {})
        step2_data = request.session.get('survey_step2', {})
        appliances_data = request.session.get('survey_appliances', [])
        
        if step == 1:
            form = SurveyStep1Form(initial=step1_data)
            template = 'homes/survey_step1.html'
            context = {
                'form': form,
                'step': 1,
                'total_steps': 3,
                'progress_percent': 33,
            }
        elif step == 2:
            if not step1_data:
                messages.warning(request, "Please complete Step 1 first.")
                return redirect('homes:survey_wizard', step=1)
            form = SurveyStep2Form(initial=step2_data)
            template = 'homes/survey_step2.html'
            context = {
                'form': form,
                'step': 2,
                'total_steps': 3,
                'progress_percent': 67,
            }
        elif step == 3:
            if not step1_data or not step2_data:
                messages.warning(request, "Please complete Steps 1 and 2 first.")
                return redirect('homes:survey_wizard', step=1)
            form = SurveyStep3ApplianceForm()
            template = 'homes/survey_step3.html'
            context = {
                'form': form,
                'step': 3,
                'total_steps': 3,
                'progress_percent': 100,
                'appliances': appliances_data,
                'appliance_count': len(appliances_data),
            }
        else:
            return redirect('homes:survey_wizard', step=1)
        
        return render(request, template, context)
    
    def post(self, request, step=1):
        """
        Process form submission for each step.
        """
        step = int(step)
        
        if step == 1:
            form = SurveyStep1Form(request.POST)
            if form.is_valid():
                # Save to session
                request.session['survey_step1'] = form.cleaned_data
                # Convert non-serializable data
                for key, value in list(request.session['survey_step1'].items()):
                    if hasattr(value, 'isoformat'):
                        request.session['survey_step1'][key] = value.isoformat()
                    elif value is None or isinstance(value, (str, int, float, bool)):
                        pass
                    else:
                        request.session['survey_step1'][key] = str(value)
                request.session.modified = True
                messages.success(request, "Step 1 complete! Let's add home features.")
                return redirect('homes:survey_wizard', step=2)
            else:
                return render(request, 'homes/survey_step1.html', {
                    'form': form,
                    'step': 1,
                    'total_steps': 3,
                    'progress_percent': 33,
                })
        
        elif step == 2:
            form = SurveyStep2Form(request.POST)
            if form.is_valid():
                # Save to session
                request.session['survey_step2'] = form.cleaned_data
                # Convert non-serializable data
                for key, value in list(request.session['survey_step2'].items()):
                    if hasattr(value, 'isoformat'):
                        request.session['survey_step2'][key] = value.isoformat()
                    elif value is None or isinstance(value, (str, int, float, bool)):
                        pass
                    else:
                        request.session['survey_step2'][key] = str(value)
                request.session.modified = True
                messages.success(request, "Step 2 complete! Now let's add your appliances (optional).")
                return redirect('homes:survey_wizard', step=3)
            else:
                return render(request, 'homes/survey_step2.html', {
                    'form': form,
                    'step': 2,
                    'total_steps': 3,
                    'progress_percent': 67,
                })
        
        elif step == 3:
            # Check if adding appliance or completing wizard
            if 'add_appliance' in request.POST:
                form = SurveyStep3ApplianceForm(request.POST)
                if form.is_valid():
                    # Add appliance to session
                    appliances = request.session.get('survey_appliances', [])
                    appliance_data = {}
                    for key, value in form.cleaned_data.items():
                        if hasattr(value, 'isoformat'):
                            appliance_data[key] = value.isoformat()
                        elif value is None or isinstance(value, (str, int, float, bool)):
                            appliance_data[key] = value
                        else:
                            appliance_data[key] = str(value)
                    appliances.append(appliance_data)
                    request.session['survey_appliances'] = appliances
                    request.session.modified = True
                    messages.success(request, f"Appliance added! You've added {len(appliances)} appliance(s).")
                    return redirect('homes:survey_wizard', step=3)
                else:
                    appliances_data = request.session.get('survey_appliances', [])
                    return render(request, 'homes/survey_step3.html', {
                        'form': form,
                        'step': 3,
                        'total_steps': 3,
                        'progress_percent': 100,
                        'appliances': appliances_data,
                        'appliance_count': len(appliances_data),
                    })
            
            elif 'complete_wizard' in request.POST:
                # Create the home with all collected data
                step1_data = request.session.get('survey_step1', {})
                step2_data = request.session.get('survey_step2', {})
                
                if not step1_data or not step2_data:
                    messages.error(request, "Missing required information. Please start over.")
                    return redirect('homes:survey_wizard', step=1)
                
                # Combine data and create home
                from datetime import date as dt_date
                home_data = {**step1_data, **step2_data}
                # Convert string dates back to date objects if needed
                for key, value in home_data.items():
                    if isinstance(value, str) and '-' in value and len(value) == 10:
                        try:
                            home_data[key] = dt_date.fromisoformat(value)
                        except:
                            pass
                
                home = Home.objects.create(owner=request.user, **home_data)
                
                # Create appliances
                appliances_data = request.session.get('survey_appliances', [])
                for appliance_data in appliances_data:
                    # Convert string dates back
                    for key, value in appliance_data.items():
                        if isinstance(value, str) and '-' in value and len(value) == 10:
                            try:
                                appliance_data[key] = dt_date.fromisoformat(value)
                            except:
                                pass
                    Appliance.objects.create(home=home, **appliance_data)
                
                # Clear session data
                request.session.pop('survey_step1', None)
                request.session.pop('survey_step2', None)
                request.session.pop('survey_appliances', None)
                request.session.modified = True
                
                messages.success(
                    request,
                    f"Home '{home.name}' created successfully with {len(appliances_data)} appliance(s)! "
                    f"You can now generate a personalized maintenance schedule."
                )
                return redirect('maintenance:generate_schedule', home_pk=home.pk)
        
        return redirect('homes:survey_wizard', step=1)
