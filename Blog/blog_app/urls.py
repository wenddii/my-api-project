from django.urls import path
from .views import PostListCreateView,PostDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]

