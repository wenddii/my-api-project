from django.urls import path,include
from .views import (
    WorkoutListCreateView, WorkoutDetailView)

urlpatterns = [
    path('workouts/', WorkoutListCreateView.as_view()),            # GET list, POST create
    path('workouts/<int:pk>/', WorkoutDetailView.as_view()),       # GET, PUT/PATCH, DELETE single
    path('api-auth/', include('rest_framework.urls')),
]