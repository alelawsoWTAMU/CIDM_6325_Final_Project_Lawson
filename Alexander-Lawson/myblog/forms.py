from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'aria-label': 'Post title',
                'aria-required': 'true'
            }),
            'author': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Select author',
                'aria-required': 'true'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...',
                'aria-label': 'Post content',
                'aria-required': 'true'
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Title is required.")
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        if len(title) > 200:
            raise forms.ValidationError("Title cannot exceed 200 characters.")
        # Check for duplicate titles (case-insensitive)
        if Post.objects.filter(title__iexact=title).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A post with this title already exists.")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Content is required.")
        if len(content) < 20:
            raise forms.ValidationError("Content must be at least 20 characters long.")
        # Check for spam-like content (all caps)
        if content.isupper() and len(content) > 50:
            raise forms.ValidationError("Please avoid using all capital letters.")
        return content
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        # Check if title appears multiple times in content (potential spam)
        if title and content:
            title_count = content.lower().count(title.lower())
            if title_count > 3:
                raise forms.ValidationError("The title appears too many times in the content. Please write more varied content.")
        
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment...',
                'aria-label': 'Comment content',
                'aria-required': 'true'
            }),
        }
        labels = {
            'content': 'Your Comment'
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(content) < 3:
            raise forms.ValidationError("Comment must be at least 3 characters long.")
        if len(content) > 1000:
            raise forms.ValidationError("Comment cannot exceed 1000 characters.")
        return content
