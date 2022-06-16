from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing), # single_pages.views.landing 함수 호출
    path('about_me/', views.about_me), # single_pages.views.about_me 함수 호출
]