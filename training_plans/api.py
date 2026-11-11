from rest_framework import viewsets

from .models import CustomPlans, TrainingPlans
from .serializers import CustomPlanSerializer, TrainingPlanSerializer


class TrainingPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Ready-made plans, the same for every user."""

    queryset = TrainingPlans.objects.prefetch_related("exercises")
    serializer_class = TrainingPlanSerializer


class CustomPlanViewSet(viewsets.ReadOnlyModelViewSet):
    """The current user's own plans; other users' plans return 404."""

    serializer_class = CustomPlanSerializer

    def get_queryset(self):
        return CustomPlans.objects.filter(user=self.request.user).prefetch_related("exercises")
