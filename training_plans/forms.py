from django import forms

from .models import CustomPlans
from exercises.models import Exercises

from django.forms import ModelForm

class CreateCustomPlanForm(forms.ModelForm):
    
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'el_form', 'placeholder':'Nazwa planu'}))
    description = forms.CharField(label='', widget=forms.Textarea(attrs={'class':'el_form', 'placeholder':'Opis planu'}))
    exercises = forms.ModelMultipleChoiceField(
        queryset=Exercises.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class':'ex_list'})
    )
    class Meta:
        model = CustomPlans
        fields = ['name', 'description', 'exercises']