from django import forms
from reg_log.models import UserWeight
from training_plans.models import TrainingPlans, CustomPlans
from itertools import chain

from datetime import date
from completed_trainings.models import Completed_Training, CompletedExercise
from exercises.models import Exercises
class AdditionalWeight(forms.ModelForm):
    
    date = date.today()
    weight = forms.FloatField(label='', widget=forms.NumberInput(attrs={
        'step': '0.01',
        'name': 'weight',
        'placeholder': 'Podaj wagę'
    }))

    class Meta:
        model = UserWeight
        fields = ['weight']

class TrainingPlanForm(forms.ModelForm):
    training_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Podaj nazwę treningu'
    }))
    plan = forms.ChoiceField(choices=[], label='')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TrainingPlanForm, self).__init__(*args, **kwargs)

        if user:
            training_plans = TrainingPlans.objects.all()
            custom_plans = CustomPlans.objects.filter(user=user)
            all_plans = list(chain(training_plans, custom_plans))
            self.fields['plan'].choices = [(plan.id, plan.name) for plan in all_plans]
    class Meta:
        model = Completed_Training
        fields = ['training_name', 'plan']

class AddExerciseForm(forms.ModelForm):
    repetitions = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Podaj ilość powtórzeń'
    }))
    weight = forms.FloatField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Podaj wagę'
    }))
    
    # exercise = forms.ChoiceField(choices=[], label='')
    exercise = forms.ModelChoiceField(queryset=Exercises.objects.none(), label='')


    class Meta:
        model = CompletedExercise
        fields = ['exercise', 'repetitions', 'weight']

    def __init__(self, *args, **kwargs):
        plan = kwargs.pop('plan', None)
        super(AddExerciseForm, self).__init__(*args, **kwargs)
        if plan:
            # self.fields['exercise'].choices = [(exercise, exercise.name) for exercise in plan.exercises.all()]

            self.fields['exercise'].queryset = plan.exercises.all()
            



    