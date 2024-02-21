from django import forms
from .models import Proteomic

class SearchForm(forms.ModelForm):
    class Meta:
        model = Proteomic
        fields = ['PGAN']
