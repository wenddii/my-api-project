from rest_framework import serializers
from .models import BlogPost, Comment
from django.contrib.auth.models import User


class CommentSerializer(serializers.ModelSerializer):
    author_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_author', 'author_full_name', 'created_at']
        read_only_fields = ['author_full_name', 'created_at']

    def get_author_full_name(self, obj):
        return f"{obj.comment_author.first_name} {obj.comment_author.last_name}"


class BlogPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # Nested comments (read-only)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']
        read_only_fields = ['created_at', 'comments']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value
