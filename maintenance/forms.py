"""
Forms for the maintenance app.
Handles schedule creation and task management.
"""

from django import forms
from .models import Schedule, MaintenanceTask
from homes.models import Home


class ScheduleForm(forms.ModelForm):
    """
    Form for creating and editing scheduled maintenance schedules.
    """
    class Meta:
        model = Schedule
        fields = [
            'scheduled_date',
            'notes',
        ]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Add notes about this maintenance schedule...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


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
