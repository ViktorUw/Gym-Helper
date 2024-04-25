from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.exercises, name='exercisesPage'),
    path('exercise/<int:exercise_id>', views.exercise, name='exPage'),
    
]