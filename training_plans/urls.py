from django.urls import path

from . import views

urlpatterns = [
    path('', views.training_plans, name='trainingPlansPage'),
    path('training_plan/<int:training_plan_id>/', views.training_plan, name='trainingPlanPage'),
    path('custom_plan/<int:custom_plan_id>/', views.custom_plan, name='customPlanPage'),
    path('create_plan/', views.create_plan, name='create_plan'),
]