# forms.py
from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Retype Password')

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'password', 'phone', 'occupation', 'instituation', 'role']


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        print(password)
        password_confirm = cleaned_data.get("password_confirm")
        print(password_confirm)


        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
