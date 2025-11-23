"""
URL patterns for the homes app.
Handles home management, appliances, and service providers.
"""

from django.urls import path
from . import views

app_name = 'homes'

urlpatterns = [
    # Home CRUD
    path('', views.HomeListView.as_view(), name='home_list'),
    path('create/', views.HomeCreateView.as_view(), name='home_create'),
    path('<int:pk>/', views.HomeDetailView.as_view(), name='home_detail'),
    path('<int:pk>/edit/', views.HomeUpdateView.as_view(), name='home_update'),
    path('<int:pk>/delete/', views.HomeDeleteView.as_view(), name='home_delete'),
    
    # Appliance management
    path('<int:home_pk>/appliances/add/', views.ApplianceCreateView.as_view(), name='appliance_create'),
    path('appliances/<int:pk>/edit/', views.ApplianceUpdateView.as_view(), name='appliance_update'),
    path('appliances/<int:pk>/delete/', views.ApplianceDeleteView.as_view(), name='appliance_delete'),
    
    # Service provider management
    path('<int:home_pk>/providers/add/', views.ServiceProviderCreateView.as_view(), name='provider_create'),
    path('providers/<int:pk>/edit/', views.ServiceProviderUpdateView.as_view(), name='provider_update'),
    path('providers/<int:pk>/delete/', views.ServiceProviderDeleteView.as_view(), name='provider_delete'),
]
