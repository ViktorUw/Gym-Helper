from django.urls import path

from . import views

urlpatterns = [
    path('', views.training_plans, name='trainingPlansPage'),
    path('training_plan/<int:training_plan_id>/', views.training_plan, name='trainingPlanPage')
    
]