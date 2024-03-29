from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView


## CBV(Class Based View)
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # template_name = 'blog/post_list.html' # ListView에서 기본 template context name은 model명소문자_list(post_list)이지만 이렇게 따로 지정해줄 수도 있음
    # context_object_name = : template에서 사용되는 context 변수명을 바꿔줄 수 있다


## FBV(Function Based View)
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     # order_by('pk') : pk 순서대로
#     # order_by('-pk') : pk 역순서대로
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )


## CBV(Class Based View)
class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html' # DetailView에서 기본 template context name은 model명소문자(post)이지만 이렇게 따로 지정해 줄 수도 있음
    # context_object_name = : template에서 사용되는 context 변수명을 바꿔줄 수 있다


## FBV(Function Based View)
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/post_detail.html',
#         {
#             'post': post,
#         }
#     )
