# forum/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('threads/', views.thread_list, name='thread_list'),
    path('threads/<slug:slug>/', views.thread_detail, name='thread_detail'),
]
