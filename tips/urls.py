"""
URL patterns for the tips app.
Handles local tips, comments, upvotes, and reporting.
"""

from django.urls import path
from . import views

app_name = 'tips'

urlpatterns = [
    # Tip browsing and creation
    path('', views.TipListView.as_view(), name='tip_list'),
    path('create/', views.TipCreateView.as_view(), name='tip_create'),
    path('<slug:slug>/', views.TipDetailView.as_view(), name='tip_detail'),
    path('<slug:slug>/edit/', views.TipUpdateView.as_view(), name='tip_update'),
    path('<slug:slug>/delete/', views.TipDeleteView.as_view(), name='tip_delete'),
    
    # Upvoting
    path('<slug:slug>/upvote/', views.TipUpvoteView.as_view(), name='tip_upvote'),
    
    # Comments
    path('<slug:slug>/comment/', views.TipCommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/delete/', views.TipCommentDeleteView.as_view(), name='comment_delete'),
    
    # Reporting
    path('<slug:slug>/report/', views.TipReportCreateView.as_view(), name='tip_report'),
    
    # Featured and filtered views
    path('category/<str:category>/', views.TipCategoryView.as_view(), name='tip_category'),
    path('location/<str:location>/', views.TipLocationView.as_view(), name='tip_location'),
]
