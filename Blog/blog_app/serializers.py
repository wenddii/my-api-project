from rest_framework import serializers 
from .models import User,Category,Post,Comment,Like

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username']

class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['name']

class PostSerializer(serializers.Serializer):
    author = UserSerializer(read_only = True)
    posts = CategorySerializer(read_only = True)
    
    class Meta: 
        mdoel = Post
        fields = ['title','author','posts']

class CommentSerializer(serializers.Serializer):
    post = PostSerializer(read_only = True,many = True)
    class Meta:
        model = Comment
        fields = ['content','author','post']