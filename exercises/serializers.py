from rest_framework import serializers

from .models import Exercises


class ExerciseSerializer(serializers.ModelSerializer):
    # The category's name instead of its id
    category = serializers.StringRelatedField()

    class Meta:
        model = Exercises
        fields = ["id", "name", "description", "category", "video"]
