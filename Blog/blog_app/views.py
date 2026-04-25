from rest_framework import generics,permissions
from .serializers import UserSerializer,CommentSerializer,PostSerializer
from .models import Post,Comment
from .permissions import IsAutherOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     permission_classes = [permissions.IsAuthenticated]

     def perform_create(self, serializer):
         serializer.save(author = self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     permission_classes = [permissions.IsAuthenticated,IsAutherOrReadOnly]
