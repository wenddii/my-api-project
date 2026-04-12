from rest_framework import generics,permissions
from .serializers import UserSerializer,CommentSerializer,PostSerializer
from .models import Post,Comment

class PostListCreateView(generics.ListCreateAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     permission_classes = permissions.IsAuthenticated
    
    def 