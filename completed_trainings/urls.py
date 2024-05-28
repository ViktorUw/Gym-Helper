from django.urls import path

from . import views


urlpatterns = [
    path('', views.completed_trainings, name='trainingsPage'),
    path('chose_training_plan/', views.chose_training_plan, name='choseTrainingPlanPage'),
    path('process_plan/', views.process_plan, name='processPlan'),
    path('ct_create_training/', views.ct_create_training, name='ct_CreateTrainingPage'),
    
    

]

