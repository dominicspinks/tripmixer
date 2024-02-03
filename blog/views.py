from django.shortcuts import render
from .models import Post

# Create your views here.
def blog_home(request):
    posts = Post.objects.filter(is_public=True)
    return render(request, 'blog/blog_home.html', { 'posts': posts})

def blog_list(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'blog/blog_list.html', { 'posts': posts})
