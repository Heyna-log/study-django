from django.shortcuts import render
from .models import Post
from django.views.generic import ListView


## CBV(Class Based View)
class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/index.html' # 기본 template name은 model명_list(post_list)이지만 이렇게 따로 지정해줄 수도 있음


## FBV(Function Based View)
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     # order_by('pk') : pk 순서대로
#     # order_by('-pk') : pk 역순서대로
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#     )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_page.html',
        {
            'post': post,
        }
    )
