from django.urls import path

from . import views


urlpatterns = [
    path('', views.completed_trainings, name='trainingsPage'),
    path('ct_create_training/<int:selected_plan>', views.ct_create_training, name='ct_create_trainingPage'),

]

