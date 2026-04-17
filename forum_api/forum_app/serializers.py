from rest_framework import serializers
from .models import Thread,Reply
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

  
class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)

    class Meta:
        model = Reply 
        fields = ['id','author']

class ThreadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    replies = ReplySerializer(many = True)
    class Meta:
        model = Thread
        fields = ['title','description','author','created_at','updated_at']
    def validate_title(self,value):
        if not value.strip():
            raise ValueError("title can't be empty")
        elif value.len() < 3:
            raise ValueError("title can't be less than three characters")
        return value
