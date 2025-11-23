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
from .models import LocalTip, TipComment, TipReport
from .forms import LocalTipForm, TipCommentForm, TipReportForm


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


class TipCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create a new tip. Only verified experts can create tips.
    """
    model = LocalTip
    form_class = LocalTipForm
    template_name = 'tips/tip_form.html'
    
    def test_func(self):
        """
        Only verified experts can create tips.
        """
        return self.request.user.is_verified_expert
    
    def handle_no_permission(self):
        """
        Redirect non-experts with helpful message.
        """
        messages.error(
            self.request,
            "Only verified local experts can share tips. Apply for expert status in your profile."
        )
        return redirect('tips:tip_list')
    
    def form_valid(self, form):
        """
        Set the author to the current user.
        """
        form.instance.author = self.request.user
        form.instance.status = 'pending'  # Requires moderation
        messages.success(
            self.request,
            "Your tip has been submitted and is pending moderator approval."
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

