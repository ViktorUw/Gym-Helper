from rest_framework import serializers

from .models import CustomPlans, TrainingPlans


class TrainingPlanSerializer(serializers.ModelSerializer):
    # Ids of the plan's exercises; details are at /api/exercises/<id>/
    exercises = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = TrainingPlans
        fields = ["id", "name", "description", "exercises"]


class CustomPlanSerializer(TrainingPlanSerializer):
    class Meta(TrainingPlanSerializer.Meta):
        model = CustomPlans
