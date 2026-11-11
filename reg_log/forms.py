from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Imię"}),
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nazwisko"}
        ),
    )
    age = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Wiek"}
        ),
    )
    email = forms.CharField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "eMail"}
        ),
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Hasło"}
        ),
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Potwierdz hasło"}
        ),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "age", "email", "password1", "password2")


class UserLogForm(forms.Form):
    email = forms.CharField(
        label="",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "email"}
        ),
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Hasło"}
        ),
    )


class AccountForm(forms.ModelForm):
    """Edit name, email and age on the profile page."""

    age = forms.IntegerField(label="Wiek", min_value=10, max_value=120, required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "age"]
        labels = {"first_name": "Imię", "last_name": "Nazwisko", "email": "Email"}
