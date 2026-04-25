from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404

from .models import Thread, ThreadVote, Comment, CommentVote
from .serializers import (
    ThreadSerializer,
    ThreadCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentDetailSerializer,
    ThreadVoteSerializer,
    CommentVoteSerializer,
)


# -------------------------
# THREADS
# -------------------------
class ThreadListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Thread.objects.all()

    def get_queryset(self):
        return (
            Thread.objects
            .select_related("author")
            .annotate(
                score=Sum("votes__value"),
                comment_count=Count("comments")
            )
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        return ThreadCreateSerializer if self.request.method == "POST" else ThreadSerializer


class ThreadDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Thread.objects.all()

    def get_queryset(self):
        return (
            Thread.objects
            .select_related("author")
            .annotate(
                score=Sum("votes__value"),
                comment_count=Count("comments")
            )
        )

    def get_serializer_class(self):
        return ThreadCreateSerializer if self.request.method in ["PUT", "PATCH"] else ThreadSerializer

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("Not allowed to edit this thread")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("Not allowed to delete this thread")
        instance.delete()


# -------------------------
# COMMENTS
# -------------------------
class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_thread(self):
        return get_object_or_404(Thread, id=self.kwargs["thread_id"])

    def get_queryset(self):
        return (
            Comment.objects
            .filter(
                thread_id=self.kwargs["thread_id"],
                parent__isnull=True
            )
            .select_related("author")
            .annotate(
                score=Sum("votes__value"),
                children_count=Count("children")
            )
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        return CommentCreateSerializer if self.request.method == "POST" else CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["thread"] = self.get_thread()
        return context


class CommentDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return (
            Comment.objects
            .select_related("author")
            .annotate(score=Sum("votes__value"))
            .prefetch_related(
                "children",
                "children__author"
            )
        )


class CommentRepliesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return (
            Comment.objects
            .filter(parent_id=self.kwargs["comment_id"])
            .select_related("author")
            .annotate(
                score=Sum("votes__value"),
                children_count=Count("children")
            )
            .order_by("created_at")
        )


# -------------------------
# VOTES
# -------------------------
class ThreadVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)

        serializer = ThreadVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ThreadVote.objects.update_or_create(
            user=request.user,
            thread=thread,
            defaults={"value": serializer.validated_data["value"]}
        )

        return Response({"status": "ok"})


class CommentVoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        serializer = CommentVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        CommentVote.objects.update_or_create(
            user=request.user,
            comment=comment,
            defaults={"value": serializer.validated_data["value"]}
        )

        return Response({"status": "ok"})