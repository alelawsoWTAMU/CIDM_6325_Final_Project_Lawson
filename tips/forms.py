"""
Forms for the tips app.
Handles tip creation, comments, and reporting.
"""

from django import forms
from django.utils.text import slugify
from .models import LocalTip, TipComment, TipReport, BlogPost, BlogComment


class LocalTipForm(forms.ModelForm):
    """
    Form for creating and editing local tips.
    """
    class Meta:
        model = LocalTip
        fields = [
            'title',
            'category',
            'content',
            'location',
            'climate_zone',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def save(self, commit=True):
        """
        Auto-generate slug from title if not provided.
        """
        instance = super().save(commit=False)
        
        if not instance.slug:
            base_slug = slugify(instance.title)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while LocalTip.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            instance.slug = slug
        
        if commit:
            instance.save()
        
        return instance


class TipCommentForm(forms.ModelForm):
    """
    Form for adding comments to tips.
    """
    class Meta:
        model = TipComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts...'}),
        }
        labels = {
            'content': 'Comment',
        }


class TipReportForm(forms.ModelForm):
    """
    Form for reporting problematic tips.
    """
    class Meta:
        model = TipReport
        fields = ['reason', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Please provide additional details...'}),
        }


class BlogPostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    """
    class Meta:
        model = BlogPost
        fields = [
            'title',
            'category',
            'excerpt',
            'content',
            'featured_image',
            'meta_description',
            'tags',
            'status',
        ]
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'meta_description': forms.Textarea(attrs={'rows': 2}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g., maintenance, winter, DIY'}),
        }
        help_texts = {
            'status': 'Save as draft to continue editing, or submit for review when ready to publish.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit status choices for non-admin users
        if self.instance and not hasattr(self.instance, '_user_is_admin'):
            self.fields['status'].choices = [
                ('draft', 'Draft'),
                ('pending', 'Submit for Review'),
            ]
    
    def save(self, commit=True):
        """Auto-generate slug from title if not provided."""
        instance = super().save(commit=False)
        
        if not instance.slug:
            base_slug = slugify(instance.title)
            slug = base_slug
            counter = 1
            
            # Ensure slug is unique
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            instance.slug = slug
        
        if commit:
            instance.save()
        
        return instance


class BlogCommentForm(forms.ModelForm):
    """
    Form for adding comments to blog posts.
    """
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts on this article...'}),
        }
        labels = {
            'content': 'Comment',
        }
