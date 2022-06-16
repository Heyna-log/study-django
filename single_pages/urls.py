from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), # blog.views.landing 함수 호출
]