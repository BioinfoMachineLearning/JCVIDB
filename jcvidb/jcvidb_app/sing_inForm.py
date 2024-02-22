# forms.py
from django import forms
from .models import User


class SignInForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Retype Password')

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data