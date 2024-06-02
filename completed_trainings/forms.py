from django import forms
from reg_log.models import UserWeight
from training_plans.models import TrainingPlans, CustomPlans
from itertools import chain

from datetime import date
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

class TrainingPlanForm(forms.Form):
    name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={
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
