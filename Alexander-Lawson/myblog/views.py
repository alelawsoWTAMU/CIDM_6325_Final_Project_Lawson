from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """
    Display a list of all blog posts ordered by creation date (newest first).
    """
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'myblog/post_list.html', context)


def post_detail(request, post_id):
    """
    Display a single blog post's full content.
    """
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'myblog/post_detail.html', context)
