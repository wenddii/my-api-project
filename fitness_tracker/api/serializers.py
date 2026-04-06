from rest_framework import serializers
from .models import Workout,Exercise
from rest_framework.fields import SerializerMethodField

class WorkoutSerializer(serializers.ModelSerializer):
    exercise = serializers.SerializerMethodField()   
    class Meta:
       fields =['user','name','date','duration','exercise']
       model = Workout

    def get_exercise(self,value):
        qs = value.exercises.all()
        return ExerciseSerialzer(qs,many = True).data
        
class ExerciseSerialzer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Exercise
