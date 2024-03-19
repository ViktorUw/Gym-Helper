from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    second_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))
    age = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Wiek'}))
    mail = forms.CharField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'eMail'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Hasło'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Potwierdz hasło'}))
    
    class Meta:
        model = User
        fields = ('username', 'second_name', 'age', 'mail', 'password1', 'password2')


class UserLogForm(forms.Form):
    # mail = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'eMail'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Hasło'}))