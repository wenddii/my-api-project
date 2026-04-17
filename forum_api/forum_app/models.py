from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="threads")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
class Reply(models.Model):
    id = models.IntegerField(unique=True)
    thread = models.ForeignKey(Thread,on_delete=models.CASCADE,related_name = "replies")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="replies")
