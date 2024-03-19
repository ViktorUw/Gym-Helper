from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.index, name='mainPage'),
    # Add more paths here
]