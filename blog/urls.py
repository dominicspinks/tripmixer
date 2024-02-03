from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('blogs/', views.blog_list, name='blog-list'),
]