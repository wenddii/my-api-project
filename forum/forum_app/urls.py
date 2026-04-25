from django.urls import path
from .views import (
    ThreadListCreateView,
    ThreadDetailView,
    CommentListCreateView,
    CommentDetailView,
    CommentRepliesView,
    ThreadVoteView,
    CommentVoteView,
)

urlpatterns = [
    # -------------------------
    # THREADS
    # -------------------------
    path("threads/", ThreadListCreateView.as_view(), name="thread-list-create"),
    path("threads/<int:pk>/", ThreadDetailView.as_view(), name="thread-detail"),

    # -------------------------
    # COMMENTS
    # -------------------------
    path(
        "threads/<int:thread_id>/comments/",
        CommentListCreateView.as_view(),
        name="comment-list-create"
    ),

    path(
        "comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail"
    ),

    path(
        "comments/<int:comment_id>/replies/",
        CommentRepliesView.as_view(),
        name="comment-replies"
    ),

    # -------------------------
    # VOTES
    # -------------------------
    path(
        "threads/<int:thread_id>/vote/",
        ThreadVoteView.as_view(),
        name="thread-vote"
    ),

    path(
        "comments/<int:comment_id>/vote/",
        CommentVoteView.as_view(),
        name="comment-vote"
    ),
]