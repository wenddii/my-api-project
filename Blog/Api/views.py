# practice viewsets views for apis
from rest_framework import generics,permissions
from .models import BlogPost,Comment
from .serializers import BlogPostSerializer,CommentSerializer

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all().order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise permissions.PermissionDenied("You cannot edit this post.")
        serializer.save()
    def perform_destroy(self,instance):
        if self.request.user != instance.author:
            raise permissions.PermissionDenied("you cannot delete this post.")
        instance.delete()