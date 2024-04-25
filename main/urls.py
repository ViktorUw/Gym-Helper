from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.index, name='mainPage'),
    path('user/', views.user_info, name='userPage'),
    path('trainings/', views.trainings, name='trainingsPage'),
    # path('training_plans/', views.training_plans, name='trainingPlansPage'),
    # Add more paths here
]