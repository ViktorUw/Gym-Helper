from rest_framework import serializers

from training_plans.models import CustomPlans

from .models import Completed_Training, CompletedExercise
from .views import series_exercises, training_summary


class SetSerializer(serializers.ModelSerializer):
    # Same limits as AddExerciseForm on the website
    repetitions = serializers.IntegerField(min_value=1, max_value=100)
    weight = serializers.FloatField(min_value=0, max_value=500)

    class Meta:
        model = CompletedExercise
        fields = ["id", "training", "exercise", "repetitions", "weight"]
        # The model allows an empty exercise, but a new set always needs one
        extra_kwargs = {"exercise": {"required": True, "allow_null": False}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and "training" in self.fields:
            # Only the user's own trainings can be chosen; any other id is "invalid"
            self.fields["training"].queryset = Completed_Training.objects.filter(
                user=request.user
            )

    def validate(self, data):
        training = data.get("training") or self.instance.training
        exercise = data.get("exercise") or self.instance.exercise
        if not series_exercises(training).filter(pk=exercise.pk).exists():
            raise serializers.ValidationError(
                {"exercise": "To ćwiczenie nie należy do planu tego treningu."}
            )
        return data


class TrainingSerializer(serializers.ModelSerializer):
    sets = SetSerializer(source="completedexercise_set", many=True, read_only=True)
    summary = serializers.SerializerMethodField()

    class Meta:
        model = Completed_Training
        fields = ["id", "training_name", "date", "training_plan", "custom_plan", "sets", "summary"]
        read_only_fields = ["date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request:
            # Only the user's own custom plans can be chosen
            self.fields["custom_plan"].queryset = CustomPlans.objects.filter(user=request.user)

    def validate(self, data):
        # Fields not sent in an update keep their current value
        current = self.instance
        training_plan = data.get("training_plan", current.training_plan if current else None)
        custom_plan = data.get("custom_plan", current.custom_plan if current else None)
        if training_plan and custom_plan:
            raise serializers.ValidationError("Podaj training_plan albo custom_plan, nie oba.")
        if current is None and not (training_plan or custom_plan):
            raise serializers.ValidationError("Podaj training_plan albo custom_plan.")
        return data

    def get_summary(self, training):
        return training_summary(list(training.completedexercise_set.all()))
