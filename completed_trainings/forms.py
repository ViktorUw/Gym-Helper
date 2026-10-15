from datetime import date

from django import forms

from completed_trainings.models import Completed_Training, CompletedExercise
from exercises.models import Exercises
from reg_log.models import UserWeight
from training_plans.models import CustomPlans, TrainingPlans


class AdditionalWeight(forms.ModelForm):
    date = date.today()
    weight = forms.FloatField(
        label="",
        widget=forms.NumberInput(
            attrs={"step": "0.01", "name": "weight", "placeholder": "Podaj wagę"}
        ),
    )

    class Meta:
        model = UserWeight
        fields = ["weight"]


class TrainingPlanForm(forms.ModelForm):
    training_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Podaj nazwę treningu"}),
    )
    plan = forms.ChoiceField(choices=[], label="")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # Prefixes keep ready ("tp") and custom ("cp") plans apart: their ids can repeat
            self.fields["plan"].choices = [
                (f"tp-{plan.id}", plan.name) for plan in TrainingPlans.objects.all()
            ] + [
                (f"cp-{plan.id}", plan.name)
                for plan in CustomPlans.objects.filter(user=user)
            ]

    class Meta:
        model = Completed_Training
        fields = ["training_name", "plan"]


class AddExerciseForm(forms.ModelForm):
    repetitions = forms.IntegerField(
        label="",
        widget=forms.NumberInput(attrs={"placeholder": "Podaj ilość powtórzeń"}),
    )
    weight = forms.FloatField(
        label="", widget=forms.NumberInput(attrs={"placeholder": "Podaj wagę"})
    )

    # exercise = forms.ChoiceField(choices=[], label='')
    exercise = forms.ModelChoiceField(queryset=Exercises.objects.none(), label="")

    class Meta:
        model = CompletedExercise
        fields = ["exercise", "repetitions", "weight"]

    def __init__(self, *args, **kwargs):
        exercises = kwargs.pop("exercises", None)
        super().__init__(*args, **kwargs)
        if exercises is not None:
            self.fields["exercise"].queryset = exercises
