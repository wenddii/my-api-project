from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Thread(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.thread}"

    @property
    def is_root(self):
        return self.parent is None

    class Meta:
        ordering = ['created_at']


class ThreadVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=[(-1, "Downvote"), (1, "Upvote")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thread')

    def __str__(self):
        return f"{self.user} voted {self.value} on {self.thread}"


class CommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=[(-1, "Downvote"), (1, "Upvote")])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f"{self.user} voted {self.value} on {self.comment}"
