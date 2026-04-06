from django.urls import path
from .views import BlogPostViewSet,CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts',BlogPostViewSet,basename='post')
