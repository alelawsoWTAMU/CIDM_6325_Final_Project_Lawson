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
    Browse all available maintenance tasks with filtering.
    """
    model = MaintenanceTask
    template_name = 'maintenance/task_list.html'
    context_object_name = 'task_list'
    paginate_by = 20
    
    def get_queryset(self):
        """
        Filter active tasks by category, difficulty, frequency, and search.
        """
        queryset = MaintenanceTask.objects.filter(is_active=True)
        
        # Category filter
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Difficulty filter
        difficulty = self.request.GET.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Frequency filter
        frequency = self.request.GET.get('frequency')
        if frequency:
            queryset = queryset.filter(frequency=frequency)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                description__icontains=search
            )
        
        # Sort
        sort = self.request.GET.get('sort', 'title')
        if sort == 'difficulty':
            queryset = queryset.order_by('difficulty')
        elif sort == 'frequency':
            queryset = queryset.order_by('frequency')
        else:  # default: alphabetical by title
            queryset = queryset.order_by('title')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Add filter choices to context.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = MaintenanceTask.CATEGORY_CHOICES
        context['difficulties'] = MaintenanceTask.DIFFICULTY_LEVELS
        context['frequencies'] = MaintenanceTask.FREQUENCY_CHOICES
        return context


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
    context_object_name = 'schedule_list'
    paginate_by = 50
    
    def get_queryset(self):
        """
        Return schedules for the user's homes.
        """
        user_homes = Home.objects.filter(owner=self.request.user)
        queryset = Schedule.objects.filter(home__in=user_homes).prefetch_related('tasks')
        
        # Filter by completion status if provided
        if self.request.GET.get('completed') == 'true':
            queryset = queryset.filter(is_completed=True)
        elif self.request.GET.get('completed') == 'false':
            queryset = queryset.filter(is_completed=False)
        
        # Filter by home if provided
        home_id = self.request.GET.get('home')
        if home_id:
            queryset = queryset.filter(home_id=home_id)
        
        return queryset
    
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
        Display the schedule generation page with applicable tasks.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        
        # Get all active tasks
        tasks = MaintenanceTask.objects.filter(is_active=True)
        
        # Filter tasks based on home characteristics
        home_age = home.get_age()
        applicable_tasks = []
        
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
            
            applicable_tasks.append(task)
        
        # Create form for schedule details
        form = ScheduleForm(user=request.user, initial={'home': home})
        
        context = {
            'home': home,
            'applicable_tasks': applicable_tasks,
            'form': form,
        }
        return render(request, 'maintenance/generate_schedule.html', context)
    
    def post(self, request, *args, **kwargs):
        """
        Create schedule with selected tasks.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        
        # Get form data
        form = ScheduleForm(request.POST, user=request.user)
        
        if not form.is_valid():
            messages.error(request, "Please correct the errors in the form.")
            return self.get(request, *args, **kwargs)
        
        # Get selected tasks
        selected_task_ids = request.POST.getlist('tasks')
        
        if not selected_task_ids:
            messages.warning(request, "Please select at least one task to include in the schedule.")
            return self.get(request, *args, **kwargs)
        
        # Create the schedule
        schedule = Schedule.objects.create(
            home=home,
            scheduled_date=form.cleaned_data['scheduled_date'],
            notes=form.cleaned_data.get('notes', ''),
            is_completed=False
        )
        
        # Add selected tasks to the schedule
        tasks = MaintenanceTask.objects.filter(id__in=selected_task_ids)
        schedule.tasks.set(tasks)
        
        messages.success(
            request,
            f"Successfully created maintenance schedule with {tasks.count()} tasks for {home.name}!"
        )
        return redirect('maintenance:schedule_detail', pk=schedule.pk)

