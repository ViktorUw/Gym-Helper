from rest_framework import viewsets

from .models import Completed_Training, CompletedExercise
from .serializers import SetSerializer, TrainingSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    """The current user's trainings with their sets and summary.

    Every query is filtered by the user, so other users' trainings return 404.
    """

    serializer_class = TrainingSerializer

    def get_queryset(self):
        return (
            Completed_Training.objects.filter(user=self.request.user)
            .prefetch_related("completedexercise_set")
            .order_by("-date", "-id")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SetViewSet(viewsets.ModelViewSet):
    """The current user's sets. Filter one training with ?training=<id>."""

    serializer_class = SetSerializer

    def get_queryset(self):
        sets = CompletedExercise.objects.filter(training__user=self.request.user)
        training = self.request.query_params.get("training")
        if training and training.isdigit():
            sets = sets.filter(training_id=training)
        return sets.order_by("id")
