from rest_framework import serializers
from .models import User,Comment,Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = ['author','content','post']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    comments = CommentSerializer(read_only = True,many = True)
    class Meta:
        model = Post
        fields = ['title','content','author','comments']
        