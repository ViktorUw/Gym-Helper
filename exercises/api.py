from rest_framework import viewsets

from .models import Exercises
from .serializers import ExerciseSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """Exercises with their category. Read only: exercises are managed in the admin."""

    queryset = Exercises.objects.select_related("category")
    serializer_class = ExerciseSerializer
