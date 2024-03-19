from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegForm(UserCreationForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nazwisko'}))
    age = forms.IntegerField(label='', widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Wiek'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'eMail'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Hasło'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Potwierdz hasło'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'age', 'email', 'password1', 'password2')


class UserLogForm(forms.Form):
    # mail = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'eMail'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Imię'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Hasło'}))