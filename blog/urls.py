from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.single_post_page), # 'blog/int형 pk/' url일때 blog.views.single_post_page 함수 호출
    path('', views.index), # blog.views.index 함수 호출
]