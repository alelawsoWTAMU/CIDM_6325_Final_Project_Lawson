"""
Forms for the maintenance app.
Handles schedule creation and task management.
"""

from django import forms
from .models import Schedule, MaintenanceTask
from homes.models import Home


class ScheduleForm(forms.ModelForm):
    """
    Form for creating and editing scheduled maintenance tasks.
    """
    class Meta:
        model = Schedule
        fields = [
            'home',
            'task',
            'scheduled_date',
            'notes',
            'recurs',
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Filter homes to only those owned by the current user.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['home'].queryset = Home.objects.filter(owner=user)
        
        # Filter to active tasks
        self.fields['task'].queryset = MaintenanceTask.objects.filter(is_active=True)


class TaskCompletionForm(forms.Form):
    """
    Form for marking a task as complete with additional details.
    """
    actual_time = forms.IntegerField(
        required=False,
        min_value=1,
        label='Actual time spent (minutes)',
        help_text='How long did it take?'
    )
    
    cost = forms.DecimalField(
        required=False,
        min_value=0,
        decimal_places=2,
        max_digits=10,
        label='Cost ($)',
        help_text='If you hired a professional'
    )
    
    performed_by = forms.CharField(
        required=False,
        max_length=200,
        label='Performed by',
        help_text='DIY or professional name'
    )
    
    feedback = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Feedback',
        help_text='Share your experience or tips'
    )
    
    rating = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=5,
        label='How helpful were the instructions?',
        help_text='Rate from 1 to 5 stars'
    )
