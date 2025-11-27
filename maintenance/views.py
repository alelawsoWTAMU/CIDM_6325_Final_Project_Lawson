"""
Views for the maintenance app.
Handles maintenance tasks, schedules, and task completions.
Uses ScheduleOptimizer for intelligent schedule generation.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, timedelta
from collections import defaultdict
from calendar import month_name
from .models import MaintenanceTask, Schedule, TaskCompletion, ScheduleTaskCompletion, ScheduleTaskCustomization
from homes.models import Home
from .forms import ScheduleForm
from .utils import ScheduleOptimizer


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
    Redirect to calendar view - calendar is now the default and only view.
    """
    def get(self, request, *args, **kwargs):
        return redirect('maintenance:schedule_calendar')


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
    
    def get_context_data(self, **kwargs):
        """
        Add today's date, completed task info, and task customizations to context.
        """
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        
        # Get completed tasks for this schedule
        completed_task_ids = ScheduleTaskCompletion.objects.filter(
            schedule=self.object
        ).values_list('task_id', flat=True)
        context['completed_task_ids'] = set(completed_task_ids)
        
        # Count pending vs completed
        total_tasks = self.object.tasks.count()
        completed_count = len(completed_task_ids)
        context['pending_count'] = total_tasks - completed_count
        context['completed_count'] = completed_count
        
        # Get or create customizations for each task in this schedule
        customizations = {}
        for task in self.object.tasks.all():
            customization, created = ScheduleTaskCustomization.objects.get_or_create(
                schedule=self.object,
                task=task
            )
            customizations[task.id] = customization
        context['task_customizations'] = customizations
        
        return context


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
            return redirect('maintenance:schedule_calendar')
        
        # Mark as complete
        schedule.mark_complete()
        
        # Create completion record
        TaskCompletion.objects.create(
            schedule=schedule,
            completed_by=request.user
        )
        
        messages.success(request, f"Task '{schedule.task.title}' marked as complete!")
        return redirect('maintenance:schedule_calendar')


class ScheduleRescheduleView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Reschedule a maintenance task to a new date.
    Supports manual date selection, quick actions (+1 week, +1 month), and AJAX drag-and-drop.
    """
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return schedule.home.owner == self.request.user
    
    def post(self, request, *args, **kwargs):
        """
        Reschedule the task to a new date.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        
        # Ensure user owns this schedule
        if schedule.home.owner != request.user:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
            messages.error(request, "You don't have permission to reschedule this task.")
            return redirect('maintenance:schedule_calendar')
        
        # Get new date from form or quick action
        new_date = None
        reason = None
        
        if 'quick_action' in request.POST:
            action = request.POST.get('quick_action')
            if action == 'week':
                new_date = schedule.scheduled_date + timedelta(weeks=1)
                reason = 'Postponed by 1 week'
            elif action == 'month':
                # Add approximately 1 month (30 days)
                new_date = schedule.scheduled_date + timedelta(days=30)
                reason = 'Postponed by 1 month'
        elif 'new_date' in request.POST:
            try:
                new_date_str = request.POST.get('new_date')
                new_date = date.fromisoformat(new_date_str)
                reason = request.POST.get('reason', 'Manually rescheduled')
            except (ValueError, TypeError):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)
                messages.error(request, "Invalid date format.")
                return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        if not new_date:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'No date provided'}, status=400)
            messages.error(request, "Please provide a new date.")
            return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        # Reschedule
        old_date = schedule.scheduled_date
        schedule.reschedule(new_date, reason)
        
        # Handle AJAX response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'old_date': old_date.isoformat(),
                'new_date': new_date.isoformat(),
                'formatted_date': new_date.strftime('%b %d, %Y')
            })
        
        # Handle standard form submission
        messages.success(
            request,
            f"Successfully rescheduled from {old_date.strftime('%b %d, %Y')} to {new_date.strftime('%b %d, %Y')}."
        )
        
        # Redirect to referrer or schedule detail
        next_url = request.POST.get('next', request.META.get('HTTP_REFERER'))
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect('maintenance:schedule_detail', pk=schedule.pk)


class GenerateScheduleView(LoginRequiredMixin, View):
    """
    Generate a personalized maintenance schedule based on home characteristics.
    This implements the core PRD requirement FR-001.
    """
    def get(self, request, *args, **kwargs):
        """
        Display the schedule generation page with intelligently recommended tasks.
        Uses ScheduleOptimizer for seasonal awareness and priority scoring.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        
        # Get recommended tasks using the optimizer (sorted by priority)
        task_priorities = ScheduleOptimizer.get_recommended_tasks(home)
        
        # Separate into priority tiers with more realistic groupings
        # Critical: 85+ (safety, essential systems, overdue)
        # High: 70-84 (important preventive maintenance)
        # Medium: 55-69 (regular seasonal tasks)
        # Low: <55 (optional/long-term maintenance)
        critical_priority = [(task, score) for task, score in task_priorities if score >= 85]
        high_priority = [(task, score) for task, score in task_priorities if 70 <= score < 85]
        medium_priority = [(task, score) for task, score in task_priorities if 55 <= score < 70]
        low_priority = [(task, score) for task, score in task_priorities if score < 55]
        
        # Get current season and climate info
        current_season = ScheduleOptimizer.get_current_season()
        climate_factor = ScheduleOptimizer.get_climate_adjustment_factor(home)
        
        # Check if "generate annual" was requested
        show_annual = request.GET.get('annual') == 'true'
        annual_schedule = None
        if show_annual:
            annual_schedule = ScheduleOptimizer.generate_annual_schedule(home)
        
        # Create form for schedule details
        form = ScheduleForm(user=request.user, initial={'home': home})
        
        context = {
            'home': home,
            'critical_priority_tasks': critical_priority,
            'high_priority_tasks': high_priority,
            'medium_priority_tasks': medium_priority,
            'low_priority_tasks': low_priority,
            'all_task_priorities': task_priorities,
            'current_season': current_season.title(),
            'climate_factor': climate_factor,
            'form': form,
            'show_annual': show_annual,
            'annual_schedule': annual_schedule,
        }
        return render(request, 'maintenance/generate_schedule.html', context)
    
    def post(self, request, *args, **kwargs):
        """
        Create schedule with selected tasks.
        Supports both single-date schedules and bulk annual generation.
        """
        home = get_object_or_404(Home, pk=self.kwargs['home_pk'], owner=request.user)
        
        # Check if bulk annual generation was requested
        if 'generate_annual' in request.POST:
            annual_items = ScheduleOptimizer.generate_annual_schedule(home)
            
            # Group tasks by date to avoid multiple schedules on same day
            tasks_by_date = {}
            for task, scheduled_date, priority in annual_items:
                if scheduled_date not in tasks_by_date:
                    tasks_by_date[scheduled_date] = []
                tasks_by_date[scheduled_date].append((task, priority))
            
            # Create one schedule per date with all tasks for that date
            created_count = 0
            for scheduled_date, task_list in sorted(tasks_by_date.items()):
                # Collect task titles for notes
                task_titles = [task.title for task, _ in task_list]
                avg_priority = sum(priority for _, priority in task_list) / len(task_list)
                
                schedule = Schedule.objects.create(
                    home=home,
                    scheduled_date=scheduled_date,
                    notes=f"Auto-generated schedule with {len(task_list)} task(s). Average Priority: {avg_priority:.0f}",
                    is_completed=False
                )
                
                # Add all tasks for this date
                for task, priority in task_list:
                    schedule.tasks.add(task)
                
                created_count += 1
            
            messages.success(
                request,
                f"Successfully generated {created_count} schedules with tasks optimized by season and climate zone ({home.get_climate_zone_display()})."
            )
            return redirect('maintenance:schedule_calendar')
        
        # Standard single-date schedule creation
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


class ScheduleCalendarView(LoginRequiredMixin, View):
    """
    Display maintenance schedules in a calendar view grouped by month.
    """
    def get(self, request, *args, **kwargs):
        """
        Render calendar view with schedules organized by month.
        """
        # Get user's homes
        user_homes = Home.objects.filter(owner=request.user)
        
        # Get schedules
        queryset = Schedule.objects.filter(home__in=user_homes).prefetch_related('tasks', 'home')
        
        # Filter by home if specified
        home_id = request.GET.get('home')
        selected_home = None
        if home_id:
            try:
                selected_home = user_homes.get(id=home_id)
                queryset = queryset.filter(home=selected_home)
            except Home.DoesNotExist:
                pass
        
        # Group schedules by month
        schedules_by_month_dict = defaultdict(list)
        
        for schedule in queryset.order_by('scheduled_date'):
            # Create key as (year, month) tuple
            key = (schedule.scheduled_date.year, schedule.scheduled_date.month)
            schedules_by_month_dict[key].append(schedule)
        
        # Convert to list of dicts for template
        schedules_by_month = []
        for (year, month), schedules in sorted(schedules_by_month_dict.items()):
            schedules_by_month.append({
                'year': year,
                'month': month,
                'month_name': month_name[month],
                'schedules': schedules,
            })
        
        context = {
            'user_homes': user_homes,
            'selected_home': selected_home,
            'schedules_by_month': schedules_by_month,
        }
        
        return render(request, 'maintenance/calendar_view.html', context)


class ScheduleRemoveTaskView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Remove a specific task from a schedule.
    """
    def test_func(self):
        """
        Ensure the user owns the home this schedule belongs to.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        return schedule.home.owner == self.request.user
    
    def post(self, request, *args, **kwargs):
        """
        Mark task as complete (keeps task visible) and auto-regenerate next occurrence.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        task_id = self.kwargs['task_id']
        
        # Ensure user owns this schedule
        if schedule.home.owner != request.user:
            messages.error(request, "You don't have permission to modify this schedule.")
            return redirect('maintenance:schedule_calendar')
        
        # Get the task
        try:
            task = MaintenanceTask.objects.get(pk=task_id)
        except MaintenanceTask.DoesNotExist:
            messages.error(request, "Task not found.")
            return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        # Calculate next due date for this task
        next_due_date = ScheduleOptimizer.generate_next_due_date(task, schedule.home, schedule.scheduled_date)
        
        # Mark task as complete (don't remove it)
        completion, created = ScheduleTaskCompletion.objects.get_or_create(
            schedule=schedule,
            task=task,
            defaults={
                'completed_by': request.user,
                'next_scheduled_date': next_due_date
            }
        )
        
        if not created:
            messages.info(request, f"Task '{task.title}' was already marked as complete.")
            return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        # Auto-regenerate this task for its next occurrence
        existing_schedule = Schedule.objects.filter(
            home=schedule.home,
            scheduled_date=next_due_date
        ).first()
        
        if existing_schedule:
            existing_schedule.tasks.add(task)
        else:
            new_schedule = Schedule.objects.create(
                home=schedule.home,
                scheduled_date=next_due_date,
                notes=f"Auto-generated: {task.title} ({task.get_frequency_display()} maintenance)",
                is_completed=False
            )
            new_schedule.tasks.add(task)
        
        messages.success(
            request,
            f"Task '{task.title}' completed and automatically rescheduled for {next_due_date.strftime('%b %d, %Y')}."
        )
        
        return redirect('maintenance:schedule_detail', pk=schedule.pk)


class ScheduleUncompleteTaskView(LoginRequiredMixin, View):
    """
    Undo task completion - mark task as pending again.
    """
    def post(self, request, *args, **kwargs):
        """
        Remove completion record and delete auto-generated future schedule.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['pk'])
        task_id = self.kwargs['task_id']
        
        # Ensure user owns this schedule
        if schedule.home.owner != request.user:
            messages.error(request, "You don't have permission to modify this schedule.")
            return redirect('maintenance:schedule_calendar')
        
        # Get the task
        try:
            task = MaintenanceTask.objects.get(pk=task_id)
        except MaintenanceTask.DoesNotExist:
            messages.error(request, "Task not found.")
            return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        # Find and delete the completion record
        try:
            completion = ScheduleTaskCompletion.objects.get(schedule=schedule, task=task)
            next_scheduled_date = completion.next_scheduled_date
            completion.delete()
            
            # Find and remove task from future schedule (if it exists and has no other tasks)
            if next_scheduled_date:
                future_schedule = Schedule.objects.filter(
                    home=schedule.home,
                    scheduled_date=next_scheduled_date
                ).first()
                
                if future_schedule:
                    future_schedule.tasks.remove(task)
                    
                    # Delete future schedule if it has no tasks left
                    if future_schedule.tasks.count() == 0:
                        future_schedule.delete()
                        messages.info(
                            request,
                            f"Auto-scheduled occurrence on {next_scheduled_date.strftime('%b %d, %Y')} was removed."
                        )
            
            messages.success(request, f"Task '{task.title}' marked as pending.")
            
        except ScheduleTaskCompletion.DoesNotExist:
            messages.info(request, f"Task '{task.title}' was not marked as complete.")
        
        return redirect('maintenance:schedule_detail', pk=schedule.pk)


class SaveTaskCustomizationView(LoginRequiredMixin, View):
    """
    Save user's custom instructions for a task in a specific schedule.
    """
    def post(self, request, *args, **kwargs):
        """
        Save or reset custom instructions.
        """
        schedule = get_object_or_404(Schedule, pk=self.kwargs['schedule_pk'])
        task_id = self.kwargs['task_id']
        
        # Ensure user owns this schedule
        if schedule.home.owner != request.user:
            messages.error(request, "You don't have permission to modify this schedule.")
            return redirect('maintenance:schedule_calendar')
        
        # Get the task
        try:
            task = MaintenanceTask.objects.get(pk=task_id)
        except MaintenanceTask.DoesNotExist:
            messages.error(request, "Task not found.")
            return redirect('maintenance:schedule_detail', pk=schedule.pk)
        
        # Get or create customization
        customization, created = ScheduleTaskCustomization.objects.get_or_create(
            schedule=schedule,
            task=task
        )
        
        # Check if user wants to reset to default
        if request.POST.get('reset') == 'true':
            customization.custom_instructions = ''
            customization.custom_description = ''
            customization.save()
            messages.success(request, f"Instructions and description for '{task.title}' reset to default.")
        else:
            # Save custom instructions and description
            custom_instructions = request.POST.get('custom_instructions', '').strip()
            custom_description = request.POST.get('custom_description', '').strip()
            customization.custom_instructions = custom_instructions
            customization.custom_description = custom_description
            customization.save()
            messages.success(request, f"Custom instructions and description saved for '{task.title}'.")
        
        return redirect('maintenance:schedule_detail', pk=schedule.pk)




