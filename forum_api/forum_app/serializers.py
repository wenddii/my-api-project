from rest_framework import serializers
from .models import Thread,Reply
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ThreadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)
    class Meta:
        model = Thread
        fields = ['title','description','author','created_at','updated_at']

class ReplySerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(read_only = True,many = True)
    author = UserSerializer(read_only = True)

    class Meta:
        model = Reply 
        fields = ['id','thread','author']
