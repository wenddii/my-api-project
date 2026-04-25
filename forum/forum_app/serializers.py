from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Sum, Count

from .models import Thread, Comment, ThreadVote, CommentVote


# -------------------------
# USER
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


# -------------------------
# THREAD
# -------------------------
class ThreadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ["title", "content"]

    def validate_title(self, value):
        if not value.strip():
            raise ValidationError("Title cannot be empty")
        return value

    def create(self, validated_data):
        return Thread.objects.create(
            author=self.context["request"].user,
            **validated_data
        )


class ThreadSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    score = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Thread
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "author",
            "score",
            "comment_count",
            "created_at",
        ]


# -------------------------
# COMMENT
# -------------------------
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    score = serializers.IntegerField(read_only=True)
    children_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "content",
            "score",
            "parent",
            "children_count",
            "created_at",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "parent"]

    def validate_content(self, value):
        if not value.strip():
            raise ValidationError("Comment cannot be empty")
        return value

    def validate(self, data):
        parent = data.get("parent")
        thread = self.context.get("thread")

        if parent:
            if parent.thread != thread:
                raise ValidationError("Parent must belong to the same thread")

        return data

    def create(self, validated_data):
        return Comment.objects.create(
            author=self.context["request"].user,
            thread=self.context["thread"],
            **validated_data
        )


# -------------------------
# COMMENT DETAIL (1-level nesting only)
# -------------------------
class CommentDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    score = serializers.IntegerField(read_only=True)
    children = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "content",
            "score",
            "created_at",
            "children",
        ]


# -------------------------
# VOTES
# -------------------------
class ThreadVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadVote
        fields = ["value"]

    def validate_value(self, value):
        if value not in [-1, 1]:
            raise ValidationError("Vote must be either +1 or -1")
        return value


class CommentVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentVote
        fields = ["value"]

    def validate_value(self, value):
        if value not in [-1, 1]:
            raise ValidationError("Vote must be either +1 or -1")
        return value