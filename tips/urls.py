"""
URL patterns for the tips app.
Handles local tips, comments, upvotes, and reporting.
"""

from django.urls import path
from . import views

app_name = 'tips'

urlpatterns = [
    # Blog posts (must come before tip slug patterns to avoid conflicts)
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/my-posts/', views.BlogMyPostsView.as_view(), name='blog_my_posts'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<slug:slug>/upvote/', views.BlogUpvoteView.as_view(), name='blog_upvote'),
    path('blog/<slug:slug>/comment/', views.BlogCommentCreateView.as_view(), name='blog_comment_create'),
    path('blog/comments/<int:pk>/delete/', views.BlogCommentDeleteView.as_view(), name='blog_comment_delete'),
    
    # Tip browsing and creation
    path('', views.TipListView.as_view(), name='tip_list'),
    path('create/', views.TipCreateView.as_view(), name='tip_create'),
    
    # Featured and filtered views
    path('category/<str:category>/', views.TipCategoryView.as_view(), name='tip_category'),
    path('location/<str:location>/', views.TipLocationView.as_view(), name='tip_location'),
    
    # Tip detail and actions (must come after specific paths)
    path('<slug:slug>/', views.TipDetailView.as_view(), name='tip_detail'),
    path('<slug:slug>/edit/', views.TipUpdateView.as_view(), name='tip_update'),
    path('<slug:slug>/delete/', views.TipDeleteView.as_view(), name='tip_delete'),
    path('<slug:slug>/upvote/', views.TipUpvoteView.as_view(), name='tip_upvote'),
    path('<slug:slug>/comment/', views.TipCommentCreateView.as_view(), name='comment_create'),
    path('<slug:slug>/report/', views.TipReportCreateView.as_view(), name='tip_report'),
    
    # Comments
    path('comments/<int:pk>/delete/', views.TipCommentDeleteView.as_view(), name='comment_delete'),
]
