from django.shortcuts import render
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-pk')
    # order_by('pk') : pk 순서대로
    # order_by('-pk') : pk 역순서대로

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )
