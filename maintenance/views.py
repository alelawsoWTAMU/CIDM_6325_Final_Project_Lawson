"""
Views for the maintenance app.
Handles maintenance tasks, schedules, and task completions.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date, timedelta
from .models import MaintenanceTask, Schedule, TaskCompletion
from homes.models import Home
from .forms import ScheduleForm


class TaskListView(ListView):
    """
    Browse all available maintenance tasks.
    """
    model = MaintenanceTask
    template_name = 'maintenance/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20
    
    def get_queryset(self):
        """
        Filter active tasks, optionally by category.
        """
        queryset = MaintenanceTask.objects.filter(is_active=True)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class TaskDetailView(DetailView):
    """
    Display detailed information about a maintenance task.
    """
    model = MaintenanceTask
    template_name = 'maintenance/task_detail.html'
    context_object_name = 'task'


class ScheduleListView(LoginRequiredMixin, ListView):
    """
    List all scheduled tasks for the user's homes.
    """
    model = Schedule
    template_name = 'maintenance/schedule_list.html'
    context_object_name = 'schedules'
    paginate_by = 50
    
    def get_queryset(self):
        """
        Return schedules for the user's homes.
        """
        user_homes = Home.objects.filter(owner=self.request.user)
        queryset = Schedule.objects.filter(home__in=user_homes)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by home if provided
        home_id = self.request.GET.get('home')
        if home_id:
            queryset = queryset.filter(home_id=home_id)
        
        return queryset.select_related('task', 'home')
    
    def get_context_data(self, **kwargs):
        """
        Add user homes to context for filtering.
        """
        context = super().get_context_data(**kwargs)
        context['user_homes'] = Home.objects.filter(owner=self.request.user)
        return context


class ScheduleDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Display details of a specific scheduled task.
    """
    model = Schedule
    template_name = 'maintenance/schedule_detail.html'
    context_object_name = 'schedule'
    
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = self.get_object()
        return schedule.home.owner == self.request.user


class ScheduleCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new scheduled task.
    """
    model = Schedule
    form_class = ScheduleForm
    template_name = 'maintenance/schedule_form.html'
    
    def get_form_kwargs(self):
        """
        Pass the current user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        """
        Redirect to schedule list after creation.
        """
        return reverse_lazy('maintenance:schedule_list')


class ScheduleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update a scheduled task.
    """
    model = Schedule
    form_class = ScheduleForm
    template_name = 'maintenance/schedule_form.html'
    
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = self.get_object()
        return schedule.home.owner == self.request.user
    
    def get_form_kwargs(self):
        """
        Pass the current user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        """
        Redirect to schedule detail after update.
        """
        return reverse_lazy('maintenance:schedule_detail', kwargs={'pk': self.object.pk})


class ScheduleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a scheduled task.
    """
    model = Schedule
    template_name = 'maintenance/schedule_confirm_delete.html'
    success_url = reverse_lazy('maintenance:schedule_list')
    
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = self.get_object()
        return schedule.home.owner == self.request.user


class ScheduleCompleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Mark a scheduled task as complete.
    """
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return schedule.home.owner == self.request.user
    
    def post(self, request, *args, **kwargs):
        """
        Mark the schedule as complete and create a completion record.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        
        # Ensure user owns this schedule
        if schedule.home.owner != request.user:
            messages.error(request, "You don't have permission to complete this task.")
            return redirect('maintenance:schedule_list')
        
        # Mark as complete
        schedule.mark_complete()
        
        # Create completion record
        TaskCompletion.objects.create(
            schedule=schedule,
            completed_by=request.user
        )
        
        messages.success(request, f"Task '{schedule.task.title}' marked as complete!")
        return redirect('maintenance:schedule_list')


class GenerateScheduleView(LoginRequiredMixin, View):
    """
    Generate a personalized maintenance schedule based on home characteristics.
    This implements the core PRD requirement FR-001.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the schedule generation page.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        context = {
            'home': home,
        }
        return render(request, 'maintenance/generate_schedule.html', context)
    
    def post(self, request, *args, **kwargs):
        """
        Generate schedule items based on home characteristics.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        
        # Get all active tasks
        tasks = MaintenanceTask.objects.filter(is_active=True)
        
        # Filter tasks based on home characteristics
        home_age = home.get_age()
        filtered_tasks = []
        
        for task in tasks:
            # Check age requirements
            if home_age > 20 and not task.applies_to_old_homes:
                continue
            if home_age <= 20 and not task.applies_to_new_homes:
                continue
            
            # Check feature requirements
            if task.requires_basement and not home.has_basement:
                continue
            if task.requires_attic and not home.has_attic:
                continue
            if task.requires_hvac and not home.has_hvac:
                continue
            if task.requires_septic and not home.has_septic:
                continue
            
            filtered_tasks.append(task)
        
        # Create schedule items
        created_count = 0
        today = date.today()
        
        for task in filtered_tasks:
            # Check if already scheduled
            if Schedule.objects.filter(home=home, task=task, status='pending').exists():
                continue
            
            # Calculate scheduled date based on frequency
            if task.frequency == 'weekly':
                scheduled_date = today + timedelta(days=7)
            elif task.frequency == 'monthly':
                scheduled_date = today + timedelta(days=30)
            elif task.frequency == 'quarterly':
                scheduled_date = today + timedelta(days=90)
            elif task.frequency == 'biannual':
                scheduled_date = today + timedelta(days=180)
            elif task.frequency == 'annual':
                scheduled_date = today + timedelta(days=365)
            elif task.frequency == 'biennial':
                scheduled_date = today + timedelta(days=730)
            else:  # as_needed
                scheduled_date = today + timedelta(days=30)
            
            # Create the schedule
            Schedule.objects.create(
                home=home,
                task=task,
                scheduled_date=scheduled_date,
                status='pending'
            )
            created_count += 1
        
        messages.success(
            request,
            f"Generated {created_count} maintenance tasks for {home.name}!"
        )
        return redirect('maintenance:schedule_list')

