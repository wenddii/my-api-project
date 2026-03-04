from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
     title=models.CharField(max_length=200)
     description = models.TextField()
     STATUS_CHOICES = [
          ('pending','Pending'),
          ('in_progress','In progress'),
          ('completed','Completed'),
     ]
     status= models.CharField(max_length=20,choices=STATUS_CHOICES)
     PRIORITY_CHOICES = [
          ('low','Low'),
          ('medium','Medium'),
          ('high','High'),
     ]
     priority = models.CharField(max_length=10,choices=PRIORITY_CHOICES)
     due_date = models.DateField()
     user=models.ForeignKey(User,on_delete=models.CASCADE)
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     
    # Create your models here.
def __str__(self):
     return self.title