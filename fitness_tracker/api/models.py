from django.db import models
from django.contrib.auth.models import User


class Workout(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='workouts')
    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(help_text="minutes spent in wrkout")
    def __str__(self):
        return self.name
    
class Exercise(models.Model):
    Workout = models.ForeignKey(Workout,on_delete=models.CASCADE,related_name='exercises')
    name = models.CharField(max_length=255)
    sets = models.IntegerField()
    reps = models.IntegerField()
