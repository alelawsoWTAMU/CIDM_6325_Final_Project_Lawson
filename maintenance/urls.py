"""
URL patterns for the maintenance app.
Handles maintenance tasks, schedules, and task completions.
"""

from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    # Task browsing
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/<slug:slug>/', views.TaskDetailView.as_view(), name='task_detail'),
    
    # Schedule management
    path('schedule/', views.ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/create/', views.ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule/<int:pk>/', views.ScheduleDetailView.as_view(), name='schedule_detail'),
    path('schedule/<int:pk>/complete/', views.ScheduleCompleteView.as_view(), name='schedule_complete'),
    path('schedule/<int:pk>/edit/', views.ScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/<int:pk>/delete/', views.ScheduleDeleteView.as_view(), name='schedule_delete'),
    
    # Generate schedule (personalized based on home)
    path('generate-schedule/<int:home_pk>/', views.GenerateScheduleView.as_view(), name='generate_schedule'),
]
