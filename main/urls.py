from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.index, name='mainPage'),
    path('user/', views.user_info, name='userPage'),
    path('user/edit/', views.edit_account, name='edit_account'),
    path('user/weight/add/', views.add_weight, name='add_weight'),
    path('user/weight/<int:weight_id>/edit/', views.edit_weight, name='edit_weight'),
    path('user/weight/<int:weight_id>/delete/', views.delete_weight, name='delete_weight'),
]
