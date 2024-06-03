from django.urls import path
from . import views

urlpatterns = [
    path('', views.completed_trainings, name='trainingsPage'),
    path('add_weight/', views.add_weight, name='add_weightPage'),
    path('chose_training_plan/', views.chose_training_plan, name='choseTrainingPlanPage'),
    path('ct_create_trainings/<int:training_id>', views.ct_create_training, name='ct_create_trainingsPage'),
    path('do_series', views.do_series, name='do_seriesPage'),
]
