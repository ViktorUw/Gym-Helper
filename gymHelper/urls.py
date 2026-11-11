"""
URL configuration for gymHelper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from completed_trainings.api import SetViewSet, TrainingViewSet
from exercises.api import ExerciseViewSet
from training_plans.api import CustomPlanViewSet, TrainingPlanViewSet

# REST API; the router creates the URLs, e.g. /api/trainings/ and /api/trainings/<id>/
router = routers.DefaultRouter()
router.register("exercises", ExerciseViewSet)
router.register("plans", TrainingPlanViewSet)
router.register("custom-plans", CustomPlanViewSet, basename="customplan")
router.register("trainings", TrainingViewSet, basename="training")
router.register("sets", SetViewSet, basename="set")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # POST {"username": <email>, "password": ...} returns {"token": ...} for apps
    path('api/token/', obtain_auth_token, name='api_token'),
    path('', include('reg_log.urls')),
    path('', include('main.urls')),
    path('exercises/', include('exercises.urls')),
    path('training/', include('training_plans.urls')),
    path('completed_trainings/', include('completed_trainings.urls')),
]
