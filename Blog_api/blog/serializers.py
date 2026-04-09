from rest_framework import serializers
from .models import Post, Comment,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content']


from rest_framework import serializers
from .models import Post, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']  # Only show the username


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Show username for comment author

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)  # Show username of the post author

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'comments']

    def create(self, validated_data):
        # Automatically assign the logged-in user as the author
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title can't be blank")
        return value