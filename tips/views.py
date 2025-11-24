"""
Views for the tips app.
Handles local tips, comments, upvotes, and reporting.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import LocalTip, TipComment, TipReport, BlogPost, BlogComment
from .forms import LocalTipForm, TipCommentForm, TipReportForm, BlogPostForm, BlogCommentForm


class TipListView(ListView):
    """
    List all approved tips with filtering options.
    """
    model = LocalTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tip_list'
    paginate_by = 20
    
    def get_queryset(self):
        """
        Return approved tips, optionally filtered.
        """
        queryset = LocalTip.objects.filter(status='approved').annotate(
            upvote_count=Count('upvotes')
        )
        
        # Filter by post type (tip or question)
        post_type = self.request.GET.get('type')
        if post_type in ['tip', 'question']:
            queryset = queryset.filter(post_type=post_type)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by location
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        # Sort
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'popular':
            queryset = queryset.order_by('-upvote_count', '-created_at')
        else:
            queryset = queryset.order_by(sort)
        
        return queryset


class TipDetailView(DetailView):
    """
    Display a single tip with comments.
    """
    model = LocalTip
    template_name = 'tips/tip_detail.html'
    context_object_name = 'tip'
    
    def get_queryset(self):
        """
        Return approved tips or tips authored by the current user.
        """
        if self.request.user.is_authenticated:
            return LocalTip.objects.filter(
                Q(status='approved') | Q(author=self.request.user)
            )
        return LocalTip.objects.filter(status='approved')
    
    def get_object(self):
        """
        Increment view count when tip is viewed.
        """
        obj = super().get_object()
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        """
        Add comments and upvote status to context.
        """
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        
        if self.request.user.is_authenticated:
            context['user_has_upvoted'] = self.object.upvotes.filter(
                id=self.request.user.id
            ).exists()
        else:
            context['user_has_upvoted'] = False
        
        return context


class TipCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new tip or question. Experts post tips, homeowners post questions.
    """
    model = LocalTip
    form_class = LocalTipForm
    template_name = 'tips/tip_form.html'
    
    def form_valid(self, form):
        """
        Set the author and post_type based on user status.
        """
        form.instance.author = self.request.user
        
        # Auto-set post_type: experts create tips, homeowners create questions
        if self.request.user.is_verified_expert:
            form.instance.post_type = 'tip'
        else:
            form.instance.post_type = 'question'
        
        form.instance.status = 'pending'  # Requires moderation
        
        post_type_label = 'tip' if form.instance.post_type == 'tip' else 'question'
        messages.success(
            self.request,
            f"Your {post_type_label} has been submitted and is pending moderator approval."
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to tip list after creation.
        """
        return reverse_lazy('tips:tip_list')


class TipUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing tip (only by author).
    """
    model = LocalTip
    form_class = LocalTipForm
    template_name = 'tips/tip_form.html'
    
    def test_func(self):
        """
        Ensure the user is the author.
        """
        tip = self.get_object()
        return tip.author == self.request.user
    
    def form_valid(self, form):
        """
        Reset status to pending if content changed.
        """
        if form.has_changed() and ('content' in form.changed_data or 'title' in form.changed_data):
            form.instance.status = 'pending'
            messages.info(
                self.request,
                "Your changes will be reviewed by moderators before being visible."
            )
        return super().form_valid(form)


class TipDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a tip (only by author).
    """
    model = LocalTip
    template_name = 'tips/tip_confirm_delete.html'
    success_url = reverse_lazy('tips:tip_list')
    
    def test_func(self):
        """
        Ensure the user is the author.
        """
        tip = self.get_object()
        return tip.author == self.request.user


class TipUpvoteView(LoginRequiredMixin, View):
    """
    Toggle upvote for a tip.
    """
    def post(self, request, *args, **kwargs):
        """
        Add or remove upvote.
        """
        tip = get_object_or_404(LocalTip, slug=self.kwargs['slug'], status='approved')
        
        if tip.upvotes.filter(id=request.user.id).exists():
            # Remove upvote
            tip.upvotes.remove(request.user)
            messages.info(request, "Upvote removed.")
        else:
            # Add upvote
            tip.upvotes.add(request.user)
            messages.success(request, "Tip upvoted!")
        
        return redirect('tips:tip_detail', slug=tip.slug)


class TipCommentCreateView(LoginRequiredMixin, CreateView):
    """
    Add a comment to a tip.
    """
    model = TipComment
    form_class = TipCommentForm
    template_name = 'tips/comment_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Get the tip being commented on.
        """
        self.tip = get_object_or_404(LocalTip, slug=self.kwargs['slug'], status='approved')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Associate comment with tip and author.
        """
        form.instance.tip = self.tip
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added!")
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the tip detail page.
        """
        return reverse_lazy('tips:tip_detail', kwargs={'slug': self.tip.slug})


class TipCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment (only by author or moderator).
    """
    model = TipComment
    template_name = 'tips/comment_confirm_delete.html'
    
    def test_func(self):
        """
        Ensure the user is the comment author or a staff member.
        """
        comment = self.get_object()
        return comment.author == self.request.user or self.request.user.is_staff
    
    def get_success_url(self):
        """
        Redirect to the tip detail page.
        """
        return reverse_lazy('tips:tip_detail', kwargs={'slug': self.object.tip.slug})


class TipReportCreateView(LoginRequiredMixin, CreateView):
    """
    Report a problematic tip.
    """
    model = TipReport
    form_class = TipReportForm
    template_name = 'tips/tip_report_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Get the tip being reported.
        """
        self.tip = get_object_or_404(LocalTip, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        Associate report with tip and reporter.
        """
        form.instance.tip = self.tip
        form.instance.reporter = self.request.user
        messages.success(
            self.request,
            "Thank you for reporting this tip. Moderators will review it."
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Redirect to the tip detail page.
        """
        return reverse_lazy('tips:tip_detail', kwargs={'slug': self.tip.slug})


class TipCategoryView(ListView):
    """
    List tips filtered by category.
    """
    model = LocalTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tips'
    paginate_by = 20
    
    def get_queryset(self):
        """
        Return tips in the specified category.
        """
        return LocalTip.objects.filter(
            status='approved',
            category=self.kwargs['category']
        ).annotate(upvote_count=Count('upvotes')).order_by('-upvote_count', '-created_at')


class TipLocationView(ListView):
    """
    List tips filtered by location.
    """
    model = LocalTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tips'
    paginate_by = 20
    
    def get_queryset(self):
        """
        Return tips for the specified location.
        """
        location = self.kwargs['location']
        return LocalTip.objects.filter(
            status='approved',
            location__icontains=location
        ).annotate(upvote_count=Count('upvotes')).order_by('-upvote_count', '-created_at')


# =============================================================================
# Blog Post Views
# =============================================================================

class BlogListView(ListView):
    """
    List all published blog posts with filtering options.
    """
    model = BlogPost
    template_name = 'tips/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Return approved/published blog posts, optionally filtered."""
        queryset = BlogPost.objects.filter(status='approved').annotate(
            upvote_count=Count('upvotes')
        )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(excerpt__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Sort
        sort = self.request.GET.get('sort', 'recent')
        if sort == 'popular':
            queryset = queryset.order_by('-upvote_count', '-published_at')
        elif sort == 'views':
            queryset = queryset.order_by('-view_count', '-published_at')
        else:  # recent
            queryset = queryset.order_by('-published_at', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = BlogPost.objects.filter(
            status='approved',
            is_featured=True
        )[:3]
        context['categories'] = BlogPost.CATEGORY_CHOICES
        return context


class BlogDetailView(DetailView):
    """
    Display a single blog post with comments.
    """
    model = BlogPost
    template_name = 'tips/blog_detail.html'
    context_object_name = 'blog_post'
    
    def get_queryset(self):
        """Only show approved blog posts."""
        return BlogPost.objects.filter(status='approved')
    
    def get_object(self):
        """Increment view count."""
        obj = super().get_object()
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author').all()
        context['comment_form'] = BlogCommentForm()
        context['user_has_upvoted'] = (
            self.request.user.is_authenticated and
            self.object.upvotes.filter(id=self.request.user.id).exists()
        )
        # Related posts
        context['related_posts'] = BlogPost.objects.filter(
            status='approved',
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create a new blog post (verified experts only).
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'tips/blog_form.html'
    
    def test_func(self):
        """Only verified experts can create blog posts."""
        return self.request.user.is_verified_expert
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            'Only verified experts can create blog posts. Please apply for expert status.'
        )
        return redirect('tips:blog_list')
    
    def form_valid(self, form):
        """Set the author to the current user."""
        form.instance.author = self.request.user
        
        # If submitting for review, set published_at
        if form.instance.status == 'pending':
            form.instance.published_at = timezone.now()
            messages.success(
                self.request,
                'Blog post submitted for review! You\'ll be notified when it\'s approved.'
            )
        else:
            messages.success(
                self.request,
                'Blog post saved as draft. You can continue editing or submit for review.'
            )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tips:blog_my_posts')


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing blog post (author only).
    """
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'tips/blog_form.html'
    
    def test_func(self):
        """Only the author can edit their blog post."""
        blog_post = self.get_object()
        return self.request.user == blog_post.author
    
    def form_valid(self, form):
        """Handle status changes."""
        old_status = self.get_object().status
        new_status = form.instance.status
        
        if old_status == 'draft' and new_status == 'pending':
            form.instance.published_at = timezone.now()
            messages.success(
                self.request,
                'Blog post submitted for review!'
            )
        else:
            messages.success(self.request, 'Blog post updated successfully!')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tips:blog_my_posts')


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post (author only).
    """
    model = BlogPost
    template_name = 'tips/blog_confirm_delete.html'
    success_url = reverse_lazy('tips:blog_my_posts')
    
    def test_func(self):
        """Only the author can delete their blog post."""
        blog_post = self.get_object()
        return self.request.user == blog_post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post deleted successfully.')
        return super().delete(request, *args, **kwargs)


class BlogMyPostsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List the current expert's blog posts (drafts, pending, approved).
    """
    model = BlogPost
    template_name = 'tips/blog_my_posts.html'
    context_object_name = 'blog_posts'
    paginate_by = 20
    
    def test_func(self):
        """Only verified experts can access this view."""
        return self.request.user.is_verified_expert
    
    def get_queryset(self):
        """Return the current user's blog posts."""
        return BlogPost.objects.filter(
            author=self.request.user
        ).order_by('-created_at')


class BlogUpvoteView(LoginRequiredMixin, View):
    """
    Toggle upvote on a blog post.
    """
    def post(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug, status='approved')
        
        if blog_post.upvotes.filter(id=request.user.id).exists():
            blog_post.upvotes.remove(request.user)
            messages.success(request, 'Upvote removed.')
        else:
            blog_post.upvotes.add(request.user)
            messages.success(request, 'Blog post upvoted!')
        
        return redirect('tips:blog_detail', slug=slug)


class BlogCommentCreateView(LoginRequiredMixin, CreateView):
    """
    Add a comment to a blog post.
    """
    model = BlogComment
    form_class = BlogCommentForm
    
    def form_valid(self, form):
        blog_post = get_object_or_404(
            BlogPost,
            slug=self.kwargs['slug'],
            status='approved'
        )
        form.instance.blog_post = blog_post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tips:blog_detail', kwargs={'slug': self.kwargs['slug']})


class BlogCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog comment (author only).
    """
    model = BlogComment
    
    def test_func(self):
        """Only the comment author can delete it."""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def get_success_url(self):
        return reverse_lazy('tips:blog_detail', kwargs={'slug': self.object.blog_post.slug})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Comment deleted successfully.')
        return super().delete(request, *args, **kwargs)

