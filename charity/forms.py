from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.models import User

class EditProfileForm(forms.Form):
    name = forms.CharField(label='Imię')
    surname=forms.CharField(label='Nazwisko')
    email = forms.CharField(label='Email', validators = [EmailValidator()])


class ChangePasswordForm(forms.Form):
    old = forms.CharField (label="Wprowadź stare hasło", widget=forms.PasswordInput)
    password = forms.CharField (label="Wprowadź nowe hasło", widget=forms.PasswordInput)
    repeat_password = forms.CharField (label="Ponownie wprowadź nowe hasło", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean ()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password != repeat_password:
            raise forms.ValidationError("Błędne hasło")


